# builder.py

**Path:** doc_gen/core/builder.py
**Syntax:** python
**Generated:** 2026-01-03 17:24:45

```python
''' DocumentationBuilder '''
"""
Documentation builder orchestration for doc-gen.
Coordinates scanning, prompting, and manifest generation.
"""

from pathlib import Path
from doc_gen.core.scanner import ProjectScanner
from doc_gen.core.config import load_config


def run_interactive_mode(project_root=None, config_path="doc-config.yml"):
    """
    Run interactive mode: scan project and build manifest.
    
    Args:
        project_root: Root directory to scan (default: current directory)
        config_path: Path to configuration file
        
    Returns:
        dict: {'success': bool, 'message': str, 'files': list}
    """
    from doc_gen.utils.prompts import prompt_file_selection
    from doc_gen.core.manifest import write_manifest
    
    # Default to current directory
    if project_root is None:
        project_root = Path.cwd()
    else:
        project_root = Path(project_root)
    
    # Load configuration
    config_result = load_config(config_path)
    if not config_result['success']:
        return {
            'success': False,
            'message': f"Could not load config: {config_result['message']}",
            'files': []
        }
    
    config = config_result['config']
    
    # Get exclusions from config
    exclusions = config.get('exclusions', [])
    
    # Determine gitignore path
    gitignore_setting = config.get('project', {}).get('gitignore', '.gitignore')
    if gitignore_setting:
        gitignore_path = project_root / gitignore_setting
    else:
        gitignore_path = None
    
    print(f"\nScanning project: {project_root}")
    print(f"Using gitignore: {gitignore_path if gitignore_path else 'None'}")
    print(f"Additional exclusions: {len(exclusions)} patterns")
    
    # Create scanner and run
    scanner = ProjectScanner(
        root_dir=project_root,
        gitignore_path=gitignore_path,
        exclusions=exclusions
    )
    
    files = scanner.scan_files()
    scanner.print_stats()
    
    if not files:
        return {
            'success': False,
            'message': 'No files found to document',
            'files': []
        }
    
    print(f"\nFound {len(files)} files to potentially document")
    
    # Interactive prompting for each file
    print("\nSelect files to include in documentation:")
    print("(Press Enter or 'y' to include, 'n' to skip)\n")
    
    selected_files = []
    for filepath in files:
        if prompt_file_selection(filepath, relative_to=project_root):
            selected_files.append(filepath)
    
    # Summary
    print(f"\n{'=' * 50}")
    print(f"Selected {len(selected_files)} of {len(files)} files")
    print('=' * 50)
    
    if not selected_files:
        return {
            'success': False,
            'message': 'No files selected for documentation',
            'files': []
        }
    
    # Get manifest output path from config
    manifest_path = config.get('output', {}).get('manifest_file', 'manifest.yml')
    
    # Write manifest
    print(f"\nWriting manifest to {manifest_path}...")
    manifest_result = write_manifest(selected_files, project_root, manifest_path)
    
    if manifest_result['success']:
        print(f"✓ {manifest_result['message']}")
    else:
        print(f"✗ {manifest_result['message']}")
        return {
            'success': False,
            'message': manifest_result['message'],
            'files': selected_files
        }
    
    return {
        'success': True,
        'message': f"Manifest created with {manifest_result['count']} files",
        'files': selected_files
    }


def run_generate_mode(manifest_path="manifest.yml", config_path="doc-config.yml"):
    """
    Run generate mode: create documentation from manifest.
    
    Args:
        manifest_path: Path to manifest file
        config_path: Path to configuration file
        
    Returns:
        dict: {'success': bool, 'message': str, 'stats': dict}
    """
    from doc_gen.core.generator import MarkdownGenerator
    
    manifest_path = Path(manifest_path)
    
    # Check if manifest exists
    if not manifest_path.exists():
        return {
            'success': False,
            'message': f'Manifest not found: {manifest_path}',
            'stats': {}
        }
    
    # Load configuration
    config_result = load_config(config_path)
    if not config_result['success']:
        return {
            'success': False,
            'message': f"Could not load config: {config_result['message']}",
            'stats': {}
        }
    
    config = config_result['config']
    
    # Get settings from config
    project_root = Path(config.get('project', {}).get('root', '.')).resolve()
    output_dir = Path(config.get('output', {}).get('base_dir', 'docs/mirror'))
    syntax_map = config.get('syntax_map', {})
    
    # Create generator and run
    generator = MarkdownGenerator(
        manifest_path=manifest_path,
        project_root=project_root,
        output_dir=output_dir,
        syntax_map=syntax_map
    )
    
    result = generator.generate_all()
    
    return result
    
def run_check_mode(manifest_path="manifest.yml"):
    """
    Run check mode: dry-run to show what would be generated.
    
    Args:
        manifest_path: Path to manifest file
        
    Returns:
        dict: {'success': bool, 'message': str}
    """
    # Placeholder
    return {
        'success': False,
        'message': 'run_check_mode() not yet implemented'
    }

```
