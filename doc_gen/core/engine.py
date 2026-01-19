"""
Core business logic API for doc-gen.

This module provides a clean interface to doc-gen's capabilities,
abstracting away internal implementation details. It serves as:

1. The primary API for UI layers (menu, CLI)
2. A catalog of doc-gen's core operations  
3. A boundary for identifying reusable utilities

Functions here delegate to appropriate internal modules (builder, config)
with consistent naming and return signatures.

All functions return: {'success': bool, 'message': str, ...}

Why this module exists:
- Provides clear, intention-revealing function names
- Hides internal module organization from UI layers
- Makes it easier to identify generally-useful functions
  that could be extracted to a separate utility library
- Single import point for all doc-gen operations
"""

from pathlib import Path
from doc_gen.core.builder import (
    run_interactive_mode,
    run_generate_mode,
    run_check_mode,
)
from doc_gen.core.config import (
    DocGenConfig,
    initialize_config as initialize_or_reset_config,
    load_config as load_configuration,
    get_ignore_patterns,
    add_ignore_pattern,
    remove_ignore_pattern,
    reset_ignore_patterns,
)


# ============================================================================
# Documentation Generation Operations
# ============================================================================

def select_manifest_files(project_path=None, config_path=None, include_patterns=None):
    """
    Scan project and interactively select files to document.
    
    This is the primary workflow for building a manifest:
    1. Scans the project filesystem (respects ignore-patterns.txt)
    2. Prompts user to select which files to include
    3. Writes selected files to .doc-gen/manifest.yml
    
    Args:
        project_path: Root directory to scan (default: current directory)
        config_path: Path to configuration file (default: .doc-gen/config.yml)
        include_patterns: Optional list of patterns to temporarily include
                         (for including normally-ignored files)
    
    Returns:
        dict: {
            'success': bool,
            'message': str,
            'files': list  # List of selected file paths
        }
    
    Example:
        >>> result = select_manifest_files()
        >>> if result['success']:
        ...     print(f"Selected {len(result['files'])} files")
    """
    return run_interactive_mode(
        project_root=project_path,
        config_path=config_path,
        include_patterns=include_patterns
    )


def generate_documentation(manifest_path=None, config_path=None):
    """
    Generate documentation from manifest.
    
    Creates markdown files for all files listed in manifest,
    with syntax highlighting and proper structure.
    
    Args:
        manifest_path: Path to manifest file (default: .doc-gen/manifest.yml)
        config_path: Path to configuration file (default: .doc-gen/config.yml)
    
    Returns:
        dict: {
            'success': bool,
            'message': str,
            'stats': dict  # Generation statistics
        }
    
    Example:
        >>> result = generate_documentation()
        >>> if result['success']:
        ...     print(f"Generated {result['stats']['total']} files")
    """
    return run_generate_mode(
        manifest_path=manifest_path,
        config_path=config_path
    )


def preview_generation(manifest_path=None, config_path=None):
    """
    Dry-run check: show what would be generated without creating files.
    
    Useful for:
    - Verifying manifest before generation
    - Checking if source files still exist
    - Reviewing output paths
    
    Args:
        manifest_path: Path to manifest file (default: .doc-gen/manifest.yml)
        config_path: Path to configuration file (default: .doc-gen/config.yml)
    
    Returns:
        dict: {
            'success': bool,
            'message': str,
            'report': str  # Detailed report text (use pager to display)
        }
    
    Example:
        >>> result = preview_generation()
        >>> if result['success']:
        ...     import pydoc
        ...     pydoc.pager(result['report'])
    """
    return run_check_mode(
        manifest_path=manifest_path,
        config_path=config_path
    )


# ============================================================================
# Configuration Management
# ============================================================================

def initialize_config(target_path=None):
    """
    Initialize or reset configuration file.
    
    Creates .doc-gen/config.yml from template.
    If file exists, prompts for confirmation before overwriting.
    
    Args:
        target_path: Where to create config (default: .doc-gen/config.yml)
    
    Returns:
        dict: {
            'success': bool,
            'message': str
        }
    
    Example:
        >>> result = initialize_config()
        >>> print(result['message'])
    """
    return initialize_or_reset_config(target_path)


def load_config(config_path=None):
    """
    Load configuration with defaults merged.
    
    Loading hierarchy (later overrides earlier):
    1. Shipped defaults.yml
    2. User's .doc-gen/config.yml
    3. Custom config (if config_path specified)
    
    Args:
        config_path: Optional custom config file path
    
    Returns:
        dict: {
            'success': bool,
            'config': dict,  # Merged configuration
            'message': str
        }
    
    Example:
        >>> result = load_config()
        >>> if result['success']:
        ...     project_name = result['config']['project']['name']
    """
    return load_configuration(config_path)


# ============================================================================
# Ignore Pattern Management
# ============================================================================

def view_ignore_patterns():
    """
    Get current ignore patterns.
    
    Returns:
        dict: {
            'success': bool,
            'patterns': list,  # List of pattern lines
            'message': str
        }
    
    Example:
        >>> result = view_ignore_patterns()
        >>> for i, pattern in enumerate(result['patterns'], 1):
        ...     print(f"{i:4d}  {pattern}")
    """
    return get_ignore_patterns()


def add_pattern(pattern):
    """
    Add new ignore pattern.
    
    Args:
        pattern: Pattern string (gitignore syntax)
    
    Returns:
        dict: {
            'success': bool,
            'message': str
        }
    
    Example:
        >>> result = add_pattern("*.log")
        >>> print(result['message'])
    """
    return add_ignore_pattern(pattern)


def remove_pattern(line_number):
    """
    Remove ignore pattern by line number.
    
    Args:
        line_number: Line to remove (1-indexed)
    
    Returns:
        dict: {
            'success': bool,
            'message': str
        }
    
    Example:
        >>> result = remove_pattern(15)
        >>> print(result['message'])
    """
    return remove_ignore_pattern(line_number)


def reset_patterns():
    """
    Reset ignore patterns to defaults.
    
    Backs up current file before resetting.
    
    Returns:
        dict: {
            'success': bool,
            'message': str
        }
    
    Example:
        >>> result = reset_patterns()
        >>> print(result['message'])
    """
    return reset_ignore_patterns()


# ============================================================================
# Utility Functions
# ============================================================================

def get_project_tree(output_name=None):
    """
    Generate filesystem tree using 'tree' command.
    
    Args:
        output_name: Output filename (default: 'project-tree.txt')
    
    Returns:
        dict: {
            'success': bool,
            'message': str,
            'output_path': Path,
            'tree_text': str
        }
    
    Note: Requires 'tree' command to be installed on system.
    
    Example:
        >>> result = get_project_tree()
        >>> if result['success']:
        ...     print(f"Tree saved to: {result['output_path']}")
    """
    import subprocess
    
    # Ensure .doc-gen structure exists
    from doc_gen.core.config import ensure_doc_gen_structure
    result = ensure_doc_gen_structure()
    if not result['success']:
        return {
            'success': False,
            'message': result['message'],
            'output_path': None,
            'tree_text': ''
        }
    
    # Default output name
    if not output_name:
        output_name = "project-tree.txt"
    
    output_path = DocGenConfig.OUTPUT_DIR / output_name
    
    # Run tree command
    try:
        proc = subprocess.run(
            ["tree", "-a", "-F"],
            check=False,
            capture_output=True,
            text=True,
        )
        
        if proc.returncode != 0 and proc.returncode != 127:
            # tree command failed (but not "command not found")
            return {
                'success': False,
                'message': f'tree command failed: {proc.stderr}',
                'output_path': None,
                'tree_text': ''
            }
        
        tree_text = proc.stdout
        
        # Save to file
        output_path.write_text(tree_text, encoding="utf-8")
        
        return {
            'success': True,
            'message': f'Tree generated: {output_path.resolve()}',
            'output_path': output_path,
            'tree_text': tree_text
        }
        
    except FileNotFoundError:
        return {
            'success': False,
            'message': "'tree' command not found. Please install it.",
            'output_path': None,
            'tree_text': ''
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Error generating tree: {str(e)}',
            'output_path': None,
            'tree_text': ''
        }


# ============================================================================
# Configuration Access (for UI layers)
# ============================================================================

def get_config_paths():
    """
    Get all standard configuration paths.
    
    Useful for UI layers that need to display paths.
    
    Returns:
        dict: {
            'doc_gen_dir': Path,
            'config_file': Path,
            'manifest_file': Path,
            'defaults_file': Path,
            'ignore_patterns': Path,
            'output_dir': Path,
            'backup_dir': Path
        }
    
    Example:
        >>> paths = get_config_paths()
        >>> print(f"Config: {paths['config_file']}")
    """
    return {
        'doc_gen_dir': DocGenConfig.DOC_GEN_DIR,
        'config_file': DocGenConfig.CONFIG_FILE,
        'manifest_file': DocGenConfig.MANIFEST_FILE,
        'defaults_file': DocGenConfig.DEFAULTS_FILE,
        'ignore_patterns': DocGenConfig.IGNORE_PATTERNS_FILE,
        'output_dir': DocGenConfig.OUTPUT_DIR,
        'backup_dir': DocGenConfig.BACKUP_DIR,
    }


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    # Documentation generation
    'select_manifest_files',
    'generate_documentation',
    'preview_generation',
    
    # Configuration
    'initialize_config',
    'load_config',
    
    # Ignore patterns
    'view_ignore_patterns',
    'add_pattern',
    'remove_pattern',
    'reset_patterns',
    
    # Utilities
    'get_project_tree',
    'get_config_paths',
    
    # Configuration class (for advanced usage)
    'DocGenConfig',
]
