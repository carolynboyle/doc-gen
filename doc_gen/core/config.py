"""
Configuration management for doc-gen.
Handles loading, validation, and initialization of configuration files.

All generated files go in .doc-gen/ directory to avoid polluting user's project.
"""

from pathlib import Path
import shutil


# Default paths - everything in .doc-gen/
DOC_GEN_DIR = Path(".doc-gen")
DEFAULT_CONFIG_PATH = DOC_GEN_DIR / "config.yml"
DEFAULT_MANIFEST_PATH = DOC_GEN_DIR / "manifest.yml"
BACKUP_DIR = DOC_GEN_DIR / "backups"
OUTPUT_DIR = DOC_GEN_DIR / "output"
IGNORE_PATTERNS_FILE = DOC_GEN_DIR / "ignore-patterns.txt"

# Hardcoded patterns that are ALWAYS excluded
HARDCODED_IGNORES = [
    '.doc-gen/',
    '.git/',
    '__pycache__/',
]


def ensure_doc_gen_structure():
    """
    Create .doc-gen/ directory structure if it doesn't exist.
    
    Creates:
        .doc-gen/
        .doc-gen/backups/
        .doc-gen/output/
        .doc-gen/ignore-patterns.txt (if missing)
    
    Returns:
        dict: {'success': bool, 'message': str}
    """
    try:
        # Create main directory
        DOC_GEN_DIR.mkdir(exist_ok=True)

        # Create subdirectories
        BACKUP_DIR.mkdir(exist_ok=True)
        OUTPUT_DIR.mkdir(exist_ok=True)
        
        # Auto-create empty manifest.yml if it doesn't exist
        manifest_path = DOC_GEN_DIR / "manifest.yml"
        if not manifest_path.exists():
            manifest_path.write_text(
                "# Auto-generated manifest - will be populated when you scan project\n"
                "documents: []\n",
                encoding='utf-8'
            )
        # Initialize ignore patterns file if it doesn't exist
        if not IGNORE_PATTERNS_FILE.exists():
            _initialize_ignore_patterns()
        
        return {
            'success': True,
            'message': f'Directory structure ready: {DOC_GEN_DIR.absolute()}'
        }
    except PermissionError as e:
        return {
            'success': False,
            'message': f'Permission denied: Cannot create {DOC_GEN_DIR.absolute()}\n  {str(e)}'
        }
    except OSError as e:
        return {
            'success': False,
            'message': f'OS error creating directory structure: {str(e)}'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Unexpected error creating directory structure: {str(e)}'
        }


def _initialize_ignore_patterns():
    """
    Initialize ignore-patterns.txt file.
    Copies from .gitignore if it exists, otherwise creates with defaults.
    Always includes hardcoded patterns at the top.
    """
    gitignore = Path('.gitignore')
    
    # Start with hardcoded patterns
    content = [
        "# ALWAYS IGNORED (hardcoded, do not remove):",
        "# These patterns are enforced by doc-gen and cannot be documented",
    ]
    content.extend(HARDCODED_IGNORES)
    content.append("")
    content.append("# Patterns below are customizable:")
    content.append("")
    
    # Add patterns from .gitignore if it exists
    if gitignore.exists():
        content.append("# Copied from .gitignore:")
        gitignore_content = gitignore.read_text().splitlines()
        content.extend(gitignore_content)
    else:
        # Add some sensible defaults
        content.extend([
            "# Common patterns to ignore:",
            "*.pyc",
            "*.pyo",
            "*.log",
            ".venv/",
            "venv/",
            ".env",
            "*.sqlite",
            "*.db",
            ".DS_Store",
        ])
    
    # Write the file
    IGNORE_PATTERNS_FILE.write_text('\n'.join(content), encoding='utf-8')


def reset_ignore_patterns():
    """
    Reset ignore-patterns.txt to defaults (from .gitignore or built-in defaults).
    
    Returns:
        dict: {'success': bool, 'message': str}
    """
    try:
        if IGNORE_PATTERNS_FILE.exists():
            # Backup the old file
            backup_name = BACKUP_DIR / f"ignore-patterns-{IGNORE_PATTERNS_FILE.stat().st_mtime:.0f}.txt"
            shutil.copy(IGNORE_PATTERNS_FILE, backup_name)
        
        _initialize_ignore_patterns()
        
        return {
            'success': True,
            'message': f'Ignore patterns reset to defaults'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Error resetting ignore patterns: {str(e)}'
        }


def add_ignore_pattern(pattern):
    """
    Add a new pattern to ignore-patterns.txt.
    
    Args:
        pattern: Pattern string to add
        
    Returns:
        dict: {'success': bool, 'message': str}
    """
    try:
        pattern = pattern.strip()
        if not pattern or pattern.startswith('#'):
            return {
                'success': False,
                'message': 'Invalid pattern (empty or comment)'
            }
        
        # Read existing patterns
        content = IGNORE_PATTERNS_FILE.read_text().splitlines()
        
        # Check if pattern already exists
        if pattern in content:
            return {
                'success': False,
                'message': f'Pattern already exists: {pattern}'
            }
        
        # Add new pattern
        content.append(pattern)
        IGNORE_PATTERNS_FILE.write_text('\n'.join(content), encoding='utf-8')
        
        return {
            'success': True,
            'message': f'Added pattern: {pattern}'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Error adding pattern: {str(e)}'
        }


def remove_ignore_pattern(line_number):
    """
    Remove a pattern from ignore-patterns.txt by line number.
    
    Args:
        line_number: Line number to remove (1-indexed)
        
    Returns:
        dict: {'success': bool, 'message': str}
    """
    try:
        content = IGNORE_PATTERNS_FILE.read_text().splitlines()
        
        if line_number < 1 or line_number > len(content):
            return {
                'success': False,
                'message': f'Invalid line number: {line_number}'
            }
        
        # Check if it's a hardcoded pattern (in first section)
        line = content[line_number - 1]
        if any(hc in line for hc in HARDCODED_IGNORES):
            return {
                'success': False,
                'message': 'Cannot remove hardcoded patterns'
            }
        
        # Remove the line
        removed = content.pop(line_number - 1)
        IGNORE_PATTERNS_FILE.write_text('\n'.join(content), encoding='utf-8')
        
        return {
            'success': True,
            'message': f'Removed: {removed}'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Error removing pattern: {str(e)}'
        }


def get_ignore_patterns():
    """
    Get current ignore patterns with line numbers.
    
    Returns:
        dict: {'success': bool, 'patterns': list, 'message': str}
    """
    try:
        if not IGNORE_PATTERNS_FILE.exists():
            return {
                'success': False,
                'message': 'Ignore patterns file not found',
                'patterns': []
            }
        
        content = IGNORE_PATTERNS_FILE.read_text().splitlines()
        
        return {
            'success': True,
            'patterns': content,
            'message': f'{len(content)} lines in ignore patterns file'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Error reading ignore patterns: {str(e)}',
            'patterns': []
        }


def initialize_config(target_path=None):
    """
    Initialize a new configuration file from template.
    
    Args:
        target_path: Path where config file should be created 
                    (default: .doc-gen/config.yml)
        
    Returns:
        dict: {'success': bool, 'message': str}
    """
    # Use default path if none specified
    if target_path is None:
        target_path = DEFAULT_CONFIG_PATH
    
    target = Path(target_path)
    
    # Ensure .doc-gen/ directory structure exists
    structure_result = ensure_doc_gen_structure()
    if not structure_result['success']:
        return structure_result
    
    # Check if config already exists
    if target.exists():
        print(f"\nWarning: {target} already exists!")
        response = input("Overwrite? (y/N): ").strip().lower()
        if response != 'y':
            return {
                'success': False,
                'message': 'Initialization cancelled by user'
            }
    
    # Find the template file
    # Template should be in project root (same dir as setup.py)
    # config.py is in doc_gen/core/, so go up two levels
    template_path = Path(__file__).parent.parent.parent / "doc-config.yml.template"
    
    if not template_path.exists():
        return {
            'success': False,
            'message': f'Template file not found at {template_path}'
        }
    
    # Copy template to target location
    try:
        shutil.copy(template_path, target)
        return {
            'success': True,
            'message': f'Configuration file created: {target.absolute()}'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Error creating config file: {str(e)}'
        }


def load_config(config_path=None):
    """
    Load and validate configuration file.
    
    Args:
        config_path: Path to configuration file (default: .doc-gen/config.yml)
        
    Returns:
        dict: {'success': bool, 'config': dict, 'message': str}
    """
    import yaml
    
    # Use default path if none specified
    if config_path is None:
        config_path = DEFAULT_CONFIG_PATH
    
    config_path = Path(config_path)
    
    # If config doesn't exist, return default config
    if not config_path.exists():
        return {
            'success': True,
            'config': _get_default_config(),
            'message': 'Using default configuration (no config file found)'
        }
    
    # Try to load the config file
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        if config is None:
            config = _get_default_config()
        
        return {
            'success': True,
            'config': config,
            'message': f'Configuration loaded from {config_path}'
        }
    except yaml.YAMLError as e:
        return {
            'success': False,
            'config': {},
            'message': f'Error parsing YAML config: {str(e)}'
        }
    except Exception as e:
        return {
            'success': False,
            'config': {},
            'message': f'Error loading config: {str(e)}'
        }


def _get_default_config():
    """
    Get default configuration when no config file exists.
    
    Returns:
        dict: Default configuration
    """
    return {
        'project': {
            'name': 'My Project',
            'root': '.'
        },
        'output': {
            'base_dir': str(OUTPUT_DIR),
            'format': 'markdown'
        },
        'syntax_map': {
            '.py': 'python',
            '.sh': 'bash',
            '.yml': 'yaml',
            '.yaml': 'yaml',
            '.json': 'json',
            '.md': 'markdown',
            '.txt': 'text',
        }
    }