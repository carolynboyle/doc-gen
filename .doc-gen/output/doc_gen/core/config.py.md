# config.py

**Path:** doc_gen/core/config.py
**Syntax:** python
**Generated:** 2026-03-26 19:01:15

```python
"""
Configuration management for doc-gen.
Handles loading, validation, and initialization of configuration files.

All generated files go in .doc-gen/ directory to avoid polluting user's project.
"""

from pathlib import Path
import shutil
import yaml


class DocGenConfig:
    """
    Single source of truth for all doc-gen configuration.
    
    This class centralizes all path constants and configuration loading logic,
    preventing the "multiple sources of truth" anti-pattern where different
    modules have different hardcoded defaults.
    
    Tool Workspace Paths (hard-coded, not user-configurable):
        - DOC_GEN_DIR: Main .doc-gen/ directory
        - CONFIG_FILE: User configuration file
        - DEFAULTS_FILE: Shipped default values
        - MANIFEST_FILE: Selected files list
        - BACKUP_DIR: Timestamped backups
        - OUTPUT_DIR: Generated documentation workspace
        - IGNORE_PATTERNS_FILE: Gitignore-style patterns
    
    Security:
        - HARDCODED_IGNORES: Always excluded, cannot be overridden
    """
    
    # Tool workspace paths - these NEVER change
    DOC_GEN_DIR = Path(".doc-gen")
    CONFIG_FILE = DOC_GEN_DIR / "config.yml"
    DEFAULTS_FILE = DOC_GEN_DIR / "defaults.yml"
    MANIFEST_FILE = DOC_GEN_DIR / "manifest.yml"
    BACKUP_DIR = DOC_GEN_DIR / "backups"
    OUTPUT_DIR = DOC_GEN_DIR / "output"
    IGNORE_PATTERNS_FILE = DOC_GEN_DIR / "ignore-patterns.txt"
    
    # Security - always excluded (enforced)
    HARDCODED_IGNORES = [
        '.doc-gen/',
        '.git/',
        '__pycache__/',
    ]
    
    @classmethod
    def load_config(cls, config_path=None):
        """
        Load configuration with proper precedence hierarchy.
        
        Precedence (later overrides earlier):
        1. Shipped defaults.yml
        2. User's .doc-gen/config.yml
        3. Custom config file (if config_path specified)
        
        Args:
            config_path: Optional path to custom config file
            
        Returns:
            dict: {'success': bool, 'config': dict, 'message': str}
        """
        # Start with defaults
        defaults = cls._load_defaults()
        
        # Determine which user config to load
        user_config_path = Path(config_path) if config_path else cls.CONFIG_FILE
        
        # Load user config if it exists
        if user_config_path.exists():
            try:
                with open(user_config_path, 'r', encoding='utf-8') as f:
                    user_config = yaml.safe_load(f) or {}
                
                # Merge user config over defaults
                config = cls._deep_merge(defaults, user_config)
                
                return {
                    'success': True,
                    'config': config,
                    'message': f'Configuration loaded from {user_config_path}'
                }
            except yaml.YAMLError as e:
                return {
                    'success': False,
                    'config': defaults,
                    'message': f'Error parsing YAML config: {str(e)}'
                }
            except Exception as e:
                return {
                    'success': False,
                    'config': defaults,
                    'message': f'Error loading config: {str(e)}'
                }
        else:
            # No user config, just use defaults
            return {
                'success': True,
                'config': defaults,
                'message': 'Using default configuration (no config file found)'
            }
    
    @classmethod
    def _load_defaults(cls):
        """
        Load defaults.yml from .doc-gen/ or package data.
        
        Returns:
            dict: Default configuration
        """
        # Try to load from .doc-gen/defaults.yml first (if copied there)
        if cls.DEFAULTS_FILE.exists():
            try:
                with open(cls.DEFAULTS_FILE, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f) or cls._get_fallback_defaults()
            except Exception:
                pass
        
        # Try to load from package data
        try:
            # defaults.yml should be in doc_gen/data/
            package_defaults = Path(__file__).parent.parent / "data" / "defaults.yml"
            if package_defaults.exists():
                with open(package_defaults, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f) or cls._get_fallback_defaults()
        except Exception:
            pass
        
        # Fall back to hardcoded defaults
        return cls._get_fallback_defaults()
    
    @classmethod
    def _get_fallback_defaults(cls):
        """
        Hardcoded fallback defaults in case defaults.yml is missing.
        
        Returns:
            dict: Minimal working configuration
        """
        return {
            'project': {
                'name': None,
                'root': '.'
            },
            'output': {
                'base_dir': str(cls.OUTPUT_DIR),
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
            },
            'exclusions': []
        }
    
    @classmethod
    def _deep_merge(cls, base, override):
        """
        Deep merge two dictionaries.
        
        Args:
            base: Base dictionary
            override: Dictionary with override values
            
        Returns:
            dict: Merged dictionary
        """
        result = base.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = cls._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result
    
    @classmethod
    def get_manifest_path(cls, config_dict=None):
        """
        Get manifest path with optional config override.
        
        Args:
            config_dict: Optional loaded configuration
            
        Returns:
            Path: Path to manifest file
        """
        if config_dict:
            custom = config_dict.get('output', {}).get('manifest_file')
            if custom:
                return Path(custom)
        return cls.MANIFEST_FILE
    
    @classmethod
    def get_project_name(cls, config_dict=None, project_root=None):
        """
        Get project name with auto-derivation from folder name.
        
        Args:
            config_dict: Optional loaded configuration
            project_root: Optional project root path
            
        Returns:
            str: Project name
        """
        # Try to get from config
        if config_dict:
            name = config_dict.get('project', {}).get('name')
            if name:
                return name
        
        # Auto-derive from folder name
        if project_root:
            return Path(project_root).resolve().name
        else:
            return Path.cwd().name


# Module-level convenience functions (backward compatibility)
# These delegate to DocGenConfig class methods

DEFAULT_CONFIG_PATH = DocGenConfig.CONFIG_FILE
DEFAULT_MANIFEST_PATH = DocGenConfig.MANIFEST_FILE
OUTPUT_DIR = DocGenConfig.OUTPUT_DIR
BACKUP_DIR = DocGenConfig.BACKUP_DIR
IGNORE_PATTERNS_FILE = DocGenConfig.IGNORE_PATTERNS_FILE
HARDCODED_IGNORES = DocGenConfig.HARDCODED_IGNORES


def ensure_doc_gen_structure():
    """
    Create .doc-gen/ directory structure if it doesn't exist.
    
    Creates:
        .doc-gen/
        .doc-gen/backups/
        .doc-gen/output/
        .doc-gen/ignore-patterns.txt (if missing)
        .doc-gen/defaults.yml (copy from package)
        .doc-gen/manifest.yml (empty template)
    
    Returns:
        dict: {'success': bool, 'message': str}
    """
    try:
        # Create main directory
        DocGenConfig.DOC_GEN_DIR.mkdir(exist_ok=True)

        # Create subdirectories
        DocGenConfig.BACKUP_DIR.mkdir(exist_ok=True)
        DocGenConfig.OUTPUT_DIR.mkdir(exist_ok=True)
        
        # Copy defaults.yml from package if not present
        if not DocGenConfig.DEFAULTS_FILE.exists():
            package_defaults = Path(__file__).parent.parent / "data" / "defaults.yml"
            if package_defaults.exists():
                shutil.copy(package_defaults, DocGenConfig.DEFAULTS_FILE)
        
        # Auto-create empty manifest.yml if it doesn't exist
        if not DocGenConfig.MANIFEST_FILE.exists():
            DocGenConfig.MANIFEST_FILE.write_text(
                "# Auto-generated manifest - will be populated when you scan project\n"
                "documents: []\n",
                encoding='utf-8'
            )
        
        # Initialize ignore patterns file if it doesn't exist
        if not DocGenConfig.IGNORE_PATTERNS_FILE.exists():
            _initialize_ignore_patterns()
        
        return {
            'success': True,
            'message': f'Directory structure ready: {DocGenConfig.DOC_GEN_DIR.absolute()}'
        }
    except PermissionError as e:
        return {
            'success': False,
            'message': f'Permission denied: Cannot create {DocGenConfig.DOC_GEN_DIR.absolute()}\n  {str(e)}'
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
    content.extend(DocGenConfig.HARDCODED_IGNORES)
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
    DocGenConfig.IGNORE_PATTERNS_FILE.write_text('\n'.join(content), encoding='utf-8')


def reset_ignore_patterns():
    """
    Reset ignore-patterns.txt to defaults (from .gitignore or built-in defaults).
    
    Returns:
        dict: {'success': bool, 'message': str}
    """
    try:
        if DocGenConfig.IGNORE_PATTERNS_FILE.exists():
            # Backup the old file
            backup_name = DocGenConfig.BACKUP_DIR / f"ignore-patterns-{DocGenConfig.IGNORE_PATTERNS_FILE.stat().st_mtime:.0f}.txt"
            shutil.copy(DocGenConfig.IGNORE_PATTERNS_FILE, backup_name)
        
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
        content = DocGenConfig.IGNORE_PATTERNS_FILE.read_text().splitlines()
        
        # Check if pattern already exists
        if pattern in content:
            return {
                'success': False,
                'message': f'Pattern already exists: {pattern}'
            }
        
        # Add new pattern
        content.append(pattern)
        DocGenConfig.IGNORE_PATTERNS_FILE.write_text('\n'.join(content), encoding='utf-8')
        
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
        content = DocGenConfig.IGNORE_PATTERNS_FILE.read_text().splitlines()
        
        if line_number < 1 or line_number > len(content):
            return {
                'success': False,
                'message': f'Invalid line number: {line_number}'
            }
        
        # Check if it's a hardcoded pattern (in first section)
        line = content[line_number - 1]
        if any(hc in line for hc in DocGenConfig.HARDCODED_IGNORES):
            return {
                'success': False,
                'message': 'Cannot remove hardcoded patterns'
            }
        
        # Remove the line
        removed = content.pop(line_number - 1)
        DocGenConfig.IGNORE_PATTERNS_FILE.write_text('\n'.join(content), encoding='utf-8')
        
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
        if not DocGenConfig.IGNORE_PATTERNS_FILE.exists():
            return {
                'success': False,
                'message': 'Ignore patterns file not found',
                'patterns': []
            }
        
        content = DocGenConfig.IGNORE_PATTERNS_FILE.read_text().splitlines()
        
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
    Initialize/reset configuration file from defaults.
    
    Args:
        target_path: Path where config file should be created 
                    (default: .doc-gen/config.yml)
        
    Returns:
        dict: {'success': bool, 'message': str}
    """
    # Use default path if none specified
    if target_path is None:
        target_path = DocGenConfig.CONFIG_FILE
    
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
    # Template should be in project root or package data
    template_path = Path(__file__).parent.parent.parent / "doc-config.yml.template"
    
    if not template_path.exists():
        # Try package data location
        template_path = Path(__file__).parent.parent / "data" / "doc-config.yml.template"
    
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
    
    This is a convenience wrapper around DocGenConfig.load_config()
    for backward compatibility.
    
    Args:
        config_path: Path to configuration file (default: .doc-gen/config.yml)
        
    Returns:
        dict: {'success': bool, 'config': dict, 'message': str}
    """
    return DocGenConfig.load_config(config_path)

```
