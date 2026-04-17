# manifest.py

**Path:** doc_gen/core/manifest.py
**Syntax:** python
**Generated:** 2026-03-26 19:01:15

```python
"""
Manifest file management for doc-gen.
Handles reading and writing manifest.yml files.
"""

from pathlib import Path
from datetime import datetime
import shutil
import yaml


def write_manifest(selected_files, project_root, output_path="manifest.yml"):
    """
    Write list of selected files to YAML manifest.
    
    Args:
        selected_files: List of Path objects (absolute or relative paths)
        project_root: Path object for project root (to make paths relative)
        output_path: Where to write manifest (default: manifest.yml)
        
    Returns:
        dict: {'success': bool, 'message': str, 'count': int}
    """
    project_root = Path(project_root).resolve()
    output_path = Path(output_path)
    
    # Backup existing manifest if it exists
    if output_path.exists():
        # Create backups directory if needed
        backup_dir = output_path.parent / 'manifest-backups'
        backup_dir.mkdir(exist_ok=True)
        
        # Create timestamped backup filename
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        backup_name = f"{timestamp}-{output_path.name}"
        backup_path = backup_dir / backup_name
        
        # Copy existing manifest to backup
        shutil.copy(output_path, backup_path)
        print(f"Backed up existing manifest to: {backup_path}")
    
    # Build manifest structure
    manifest = {
        'version': 1,
        'documents': []
    }
    
    # Convert to relative paths and add to manifest
    for filepath in selected_files:
        filepath = Path(filepath)
        
        # If already relative, use as-is; otherwise make it relative
        if filepath.is_absolute():
            try:
                rel_path = filepath.relative_to(project_root)
            except ValueError:
                # File is outside project root, skip it
                continue
        else:
            rel_path = filepath
        
        manifest['documents'].append({
            'path': str(rel_path)
        })
    
    # Write to file (AFTER processing all files)
    try:
        with output_path.open('w') as f:
            # Add timestamp comment at top
            f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Project: {project_root}\n")
            f.write(f"# Files: {len(manifest['documents'])}\n\n")
            
            # Write YAML
            yaml.dump(manifest, f, default_flow_style=False, sort_keys=False)
        
        return {
            'success': True,
            'message': f'Manifest written to {output_path.absolute()}',
            'count': len(manifest['documents'])
        }
    
    except Exception as e:
        return {
            'success': False,
            'message': f'Error writing manifest: {str(e)}',
            'count': 0
        }


def read_manifest(manifest_path="manifest.yml"):
    """
    Read and validate manifest file.
    
    Args:
        manifest_path: Path to manifest file
        
    Returns:
        dict: {'success': bool, 'documents': list, 'message': str}
    """
    manifest_path = Path(manifest_path)
    
    if not manifest_path.exists():
        return {
            'success': False,
            'documents': [],
            'message': f'Manifest not found: {manifest_path}'
        }
    
    try:
        with manifest_path.open('r') as f:
            manifest = yaml.safe_load(f)
        
        # Validate structure
        if not isinstance(manifest, dict):
            return {
                'success': False,
                'documents': [],
                'message': 'Invalid manifest format: not a dictionary'
            }
        
        if 'documents' not in manifest:
            return {
                'success': False,
                'documents': [],
                'message': 'Invalid manifest: missing "documents" key'
            }
        
        # Extract file paths
        documents = [doc['path'] for doc in manifest['documents'] if 'path' in doc]
        
        return {
            'success': True,
            'documents': documents,
            'message': f'Loaded {len(documents)} files from manifest'
        }
    
    except yaml.YAMLError as e:
        return {
            'success': False,
            'documents': [],
            'message': f'YAML parse error: {str(e)}'
        }
    except Exception as e:
        return {
            'success': False,
            'documents': [],
            'message': f'Error reading manifest: {str(e)}'
        }
```
