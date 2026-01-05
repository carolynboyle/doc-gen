# config.py

**Path:** doc_gen/core/config.py
**Syntax:** python
**Generated:** 2026-01-03 17:24:45

```python
"""
Configuration management for doc-gen.
Handles loading, validation, and initialization of configuration files.
"""

from pathlib import Path
import shutil
import yaml


def initialize_config(target_path="doc-config.yml"):
    """
    Initialize a new configuration file from template.
    
    Args:
        target_path: Path where config file should be created (default: doc-config.yml)
        
    Returns:
        dict: {'success': bool, 'message': str}
    """
    target = Path(target_path)
    
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


def load_config(config_path="doc-config.yml"):
    """
    Load and validate configuration file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        dict: {'success': bool, 'config': dict or None, 'message': str}
    """
    config_file = Path(config_path)
    
    # Check if config file exists
    if not config_file.exists():
        return {
            'success': False,
            'config': None,
            'message': f'Config file not found: {config_file.absolute()}'
        }
    
    # Try to load YAML
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        # Basic validation - should at least be a dict
        if not isinstance(config, dict):
            return {
                'success': False,
                'config': None,
                'message': 'Invalid config format: expected YAML dictionary'
            }
        
        return {
            'success': True,
            'config': config,
            'message': f'Configuration loaded from {config_file.absolute()}'
        }
        
    except yaml.YAMLError as e:
        return {
            'success': False,
            'config': None,
            'message': f'YAML parse error: {str(e)}'
        }
    except Exception as e:
        return {
            'success': False,
            'config': None,
            'message': f'Error reading config: {str(e)}'
        }
```
