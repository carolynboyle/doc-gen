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


def ensure_doc_gen_structure():
    """
    Create .doc-gen/ directory structure if it doesn't exist.
    
    Creates:
        .doc-gen/
        .doc-gen/backups/
        .doc-gen/output/
    
    Returns:
        dict: {'success': bool, 'message': str}
    """
    try:
        # Create main directory
        DOC_GEN_DIR.mkdir(exist_ok=True)
        
        # Create subdirectories
        BACKUP_DIR.mkdir(exist_ok=True)
        OUTPUT_DIR.mkdir(exist_ok=True)
        
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
    
    config_file = Path(config_path)
    
    # If config doesn't exist, create it with defaults
    if not config_file.exists():
        init_result = initialize_config(config_path)
        if not init_result['success']:
            return init_result
    
    # Load the YAML file
    try:
        with open(config_file, 'r') as f:
            config_data = yaml.safe_load(f)
        
        return {
            'success': True,
            'config': config_data,
            'message': f'Config loaded from {config_file}'
        }
    except Exception as e:
        return {
            'success': False,
            'config': {},
            'message': f'Error loading config: {str(e)}'
        }