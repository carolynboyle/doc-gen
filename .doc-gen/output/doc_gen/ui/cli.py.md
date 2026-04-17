# cli.py

**Path:** doc_gen/ui/cli.py
**Syntax:** python
**Generated:** 2026-03-26 19:01:15

```python
''' ArgumentParser, CLI handlers '''
"""
Command-line interface for doc-gen.
Provides scriptable, non-interactive access to all doc-gen operations.
"""

import argparse
import sys
from pathlib import Path

from doc_gen.core import engine
from doc_gen.core.config import DocGenConfig


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog='doc-gen',
        description='Generate syntax-highlighted documentation from source code',
        epilog='For interactive menu mode, run doc-gen without arguments'
    )
    
    # Global options
    parser.add_argument(
        '--config',
        metavar='PATH',
        help='Path to configuration file (default: .doc-gen/config.yml)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='doc-gen 0.1.0'
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(
        dest='command',
        help='Available commands'
    )
    
    # ========================================================================
    # scan - Select files for documentation
    # ========================================================================
    scan_parser = subparsers.add_parser(
        'scan',
        help='Scan project and select files to document'
    )
    scan_parser.add_argument(
        'project',
        nargs='?',
        default='.',
        help='Project directory to scan (default: current directory)'
    )
    scan_parser.add_argument(
        '--include',
        nargs='+',
        metavar='PATTERN',
        help='Temporarily include ignored patterns'
    )
    
    # ========================================================================
    # generate - Create documentation
    # ========================================================================
    generate_parser = subparsers.add_parser(
        'generate',
        help='Generate documentation from manifest'
    )
    generate_parser.add_argument(
        '--manifest',
        metavar='PATH',
        help='Path to manifest file (default: .doc-gen/manifest.yml)'
    )
    
    # ========================================================================
    # check - Dry run preview
    # ========================================================================
    check_parser = subparsers.add_parser(
        'check',
        help='Preview what would be generated (dry run)'
    )
    check_parser.add_argument(
        '--manifest',
        metavar='PATH',
        help='Path to manifest file (default: .doc-gen/manifest.yml)'
    )
    check_parser.add_argument(
        '--save',
        metavar='FILE',
        help='Save report to file instead of displaying'
    )
    
    # ========================================================================
    # tree - Generate filesystem tree
    # ========================================================================
    tree_parser = subparsers.add_parser(
        'tree',
        help='Generate project filesystem tree'
    )
    tree_parser.add_argument(
        '--output',
        metavar='FILE',
        help='Output filename (default: project-tree.txt)'
    )
    tree_parser.add_argument(
        '--display',
        action='store_true',
        help='Display tree in terminal (in addition to saving)'
    )
    
    # ========================================================================
    # config - Configuration management
    # ========================================================================
    config_parser = subparsers.add_parser(
        'config',
        help='Manage configuration'
    )
    config_subparsers = config_parser.add_subparsers(
        dest='config_action',
        help='Configuration actions'
    )
    
    # config init
    config_subparsers.add_parser(
        'init',
        help='Initialize/reset configuration file'
    )
    
    # config view
    config_subparsers.add_parser(
        'view',
        help='Display current configuration'
    )
    
    # config paths
    config_subparsers.add_parser(
        'paths',
        help='Show all configuration file paths'
    )
    
    # ========================================================================
    # patterns - Manage ignore patterns
    # ========================================================================
    patterns_parser = subparsers.add_parser(
        'patterns',
        help='Manage ignore patterns'
    )
    patterns_subparsers = patterns_parser.add_subparsers(
        dest='patterns_action',
        help='Pattern actions'
    )
    
    # patterns list
    patterns_subparsers.add_parser(
        'list',
        help='List current ignore patterns'
    )
    
    # patterns add
    add_parser = patterns_subparsers.add_parser(
        'add',
        help='Add new ignore pattern'
    )
    add_parser.add_argument(
        'pattern',
        help='Pattern to add (e.g., *.log or .venv/)'
    )
    
    # patterns remove
    remove_parser = patterns_subparsers.add_parser(
        'remove',
        help='Remove ignore pattern by line number'
    )
    remove_parser.add_argument(
        'line',
        type=int,
        help='Line number to remove (1-indexed)'
    )
    
    # patterns reset
    patterns_subparsers.add_parser(
        'reset',
        help='Reset patterns to defaults'
    )
    
    # ========================================================================
    # Parse and execute
    # ========================================================================
    args = parser.parse_args()
    
    # If no command given, show help
    if not args.command:
        parser.print_help()
        return 0
    
    # Execute the appropriate command
    try:
        if args.command == 'scan':
            return cmd_scan(args)
        elif args.command == 'generate':
            return cmd_generate(args)
        elif args.command == 'check':
            return cmd_check(args)
        elif args.command == 'tree':
            return cmd_tree(args)
        elif args.command == 'config':
            return cmd_config(args)
        elif args.command == 'patterns':
            return cmd_patterns(args)
        else:
            parser.print_help()
            return 1
    except KeyboardInterrupt:
        print("\n\nInterrupted by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


# ============================================================================
# Command Implementations
# ============================================================================

def cmd_scan(args):
    """Execute scan command."""
    print(f"Scanning project: {args.project}")
    
    result = engine.select_manifest_files(
        project_path=args.project if args.project != '.' else None,
        config_path=args.config,
        include_patterns=args.include
    )
    
    if result['success']:
        print(f"✓ {result['message']}")
        print(f"  Selected {len(result['files'])} files")
        return 0
    else:
        print(f"✗ {result['message']}", file=sys.stderr)
        return 1


def cmd_generate(args):
    """Execute generate command."""
    result = engine.generate_documentation(
        manifest_path=args.manifest,
        config_path=args.config
    )
    
    if result['success']:
        print(f"✓ {result['message']}")
        if 'stats' in result:
            stats = result['stats']
            print(f"  Files generated: {stats.get('total', 0)}")
        return 0
    else:
        print(f"✗ {result['message']}", file=sys.stderr)
        return 1


def cmd_check(args):
    """Execute check command."""
    result = engine.preview_generation(
        manifest_path=args.manifest,
        config_path=args.config
    )
    
    if result['success']:
        if args.save:
            # Save to file
            try:
                Path(args.save).write_text(result['report'], encoding='utf-8')
                print(f"✓ Report saved to: {Path(args.save).resolve()}")
                return 0
            except Exception as e:
                print(f"✗ Error saving report: {e}", file=sys.stderr)
                return 1
        else:
            # Display in terminal
            print(result['report'])
            return 0
    else:
        print(f"✗ {result['message']}", file=sys.stderr)
        return 1


def cmd_tree(args):
    """Execute tree command."""
    result = engine.get_project_tree(output_name=args.output)
    
    if result['success']:
        print(f"✓ {result['message']}")
        
        if args.display:
            print("\n" + "=" * 70)
            print(result['tree_text'])
            print("=" * 70)
        
        return 0
    else:
        print(f"✗ {result['message']}", file=sys.stderr)
        return 1


def cmd_config(args):
    """Execute config command."""
    if not args.config_action:
        print("Error: config command requires an action", file=sys.stderr)
        print("Usage: doc-gen config {init|view|paths}", file=sys.stderr)
        return 1
    
    if args.config_action == 'init':
        result = engine.initialize_config()
        if result['success']:
            print(f"✓ {result['message']}")
            return 0
        else:
            print(f"✗ {result['message']}", file=sys.stderr)
            return 1
    
    elif args.config_action == 'view':
        result = engine.load_config(args.config)
        if result['success']:
            import yaml
            print(yaml.dump(result['config'], default_flow_style=False, sort_keys=False))
            return 0
        else:
            print(f"✗ {result['message']}", file=sys.stderr)
            return 1
    
    elif args.config_action == 'paths':
        paths = engine.get_config_paths()
        print("Doc-Gen Configuration Paths:")
        print(f"  .doc-gen directory:  {paths['doc_gen_dir'].resolve()}")
        print(f"  Config file:         {paths['config_file'].resolve()}")
        print(f"  Defaults file:       {paths['defaults_file'].resolve()}")
        print(f"  Manifest file:       {paths['manifest_file'].resolve()}")
        print(f"  Ignore patterns:     {paths['ignore_patterns'].resolve()}")
        print(f"  Output directory:    {paths['output_dir'].resolve()}")
        print(f"  Backup directory:    {paths['backup_dir'].resolve()}")
        return 0
    
    return 1


def cmd_patterns(args):
    """Execute patterns command."""
    if not args.patterns_action:
        print("Error: patterns command requires an action", file=sys.stderr)
        print("Usage: doc-gen patterns {list|add|remove|reset}", file=sys.stderr)
        return 1
    
    if args.patterns_action == 'list':
        result = engine.view_ignore_patterns()
        if result['success']:
            for i, line in enumerate(result['patterns'], 1):
                # Mark hardcoded patterns
                if any(hc in line for hc in DocGenConfig.HARDCODED_IGNORES) and not line.startswith('#'):
                    print(f"{i:4d}  {line}  [HARDCODED]")
                else:
                    print(f"{i:4d}  {line}")
            return 0
        else:
            print(f"✗ {result['message']}", file=sys.stderr)
            return 1
    
    elif args.patterns_action == 'add':
        result = engine.add_pattern(args.pattern)
        if result['success']:
            print(f"✓ {result['message']}")
            return 0
        else:
            print(f"✗ {result['message']}", file=sys.stderr)
            return 1
    
    elif args.patterns_action == 'remove':
        result = engine.remove_pattern(args.line)
        if result['success']:
            print(f"✓ {result['message']}")
            return 0
        else:
            print(f"✗ {result['message']}", file=sys.stderr)
            return 1
    
    elif args.patterns_action == 'reset':
        # Confirm before resetting
        print("This will reset ignore patterns to defaults.")
        print("Current patterns will be backed up.")
        confirm = input("Continue? (y/N): ").strip().lower()
        
        if confirm == 'y':
            result = engine.reset_patterns()
            if result['success']:
                print(f"✓ {result['message']}")
                return 0
            else:
                print(f"✗ {result['message']}", file=sys.stderr)
                return 1
        else:
            print("Reset cancelled")
            return 0
    
    return 1


if __name__ == '__main__':
    sys.exit(main())

```
