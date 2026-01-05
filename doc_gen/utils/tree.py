"""
Project tree visualization for doc-gen.
Generates directory tree structures from file lists.
"""

from pathlib import Path
from collections import defaultdict


def build_tree_structure(file_paths, project_root):
    """
    Build nested dictionary tree structure from file paths.
    
    Args:
        file_paths: List of Path objects or strings
        project_root: Root directory path
        
    Returns:
        dict: Nested dictionary representing tree structure
    """
    tree = {}
    
    for filepath in file_paths:
        # Convert to Path and make relative
        path = Path(filepath)
        if path.is_absolute():
            try:
                path = path.relative_to(project_root)
            except ValueError:
                continue
        
        # Split into parts
        parts = path.parts
        
        # Build nested dict
        current = tree
        for i, part in enumerate(parts):
            if i == len(parts) - 1:
                # Leaf (file)
                current[part] = None
            else:
                # Branch (directory)
                if part not in current:
                    current[part] = {}
                current = current[part]
    
    return tree


def format_tree(tree, prefix="", is_last=True, root_name=None):
    """
    Format tree structure as string with box-drawing characters.
    
    Args:
        tree: Nested dictionary from build_tree_structure()
        prefix: Current line prefix (for recursion)
        is_last: Whether this is the last item in parent (for recursion)
        root_name: Name to display for root (optional)
        
    Returns:
        list: Lines of formatted tree
    """
    lines = []
    
    # Handle root display
    if root_name and prefix == "":
        lines.append(f"{root_name}/")
        prefix = ""
    
    items = sorted(tree.items())
    
    for i, (name, subtree) in enumerate(items):
        is_last_item = (i == len(items) - 1)
        
        # Determine connector
        if prefix == "":
            connector = "├── " if not is_last_item else "└── "
        else:
            connector = "├── " if not is_last_item else "└── "
        
        # Add directory indicator
        display_name = f"{name}/" if subtree is not None else name
        
        # Add this line
        lines.append(f"{prefix}{connector}{display_name}")
        
        # Recurse for directories
        if subtree is not None:
            # Determine new prefix
            if prefix == "":
                new_prefix = "│   " if not is_last_item else "    "
            else:
                extension = "│   " if not is_last_item else "    "
                new_prefix = prefix + extension
            
            lines.extend(format_tree(subtree, new_prefix, is_last_item))
    
    return lines


def generate_project_tree(file_paths, project_root, project_name=None):
    """
    Generate formatted project tree from file paths.
    
    Args:
        file_paths: List of file paths (Path objects or strings)
        project_root: Root directory path
        project_name: Name to display for root (default: directory name)
        
    Returns:
        str: Formatted tree structure
    """
    project_root = Path(project_root)
    
    if project_name is None:
        project_name = project_root.name
    
    # Build tree structure
    tree = build_tree_structure(file_paths, project_root)
    
    # Format as string
    lines = format_tree(tree, root_name=project_name)
    
    return "\n".join(lines)


def save_project_tree(file_paths, project_root, output_path="PROJECT_STRUCTURE.txt", project_name=None):
    """
    Generate and save project tree to file.
    
    Args:
        file_paths: List of file paths
        project_root: Root directory path
        output_path: Where to save tree file
        project_name: Name to display for root
        
    Returns:
        dict: {'success': bool, 'message': str, 'path': Path}
    """
    try:
        tree_text = generate_project_tree(file_paths, project_root, project_name)
        
        # Add header
        from datetime import datetime
        output = []
        output.append("# Project Structure")
        output.append(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append(f"# Root: {Path(project_root).resolve()}")
        output.append(f"# Files: {len(file_paths)}")
        output.append("")
        output.append(tree_text)
        output.append("")
        
        output_path = Path(output_path)
        output_path.write_text("\n".join(output), encoding='utf-8')
        
        return {
            'success': True,
            'message': f'Project tree saved to {output_path.absolute()}',
            'path': output_path
        }
    
    except Exception as e:
        return {
            'success': False,
            'message': f'Error saving project tree: {str(e)}',
            'path': None
        }