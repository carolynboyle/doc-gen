# prompts.py

**Path:** doc_gen/utils/prompts.py
**Syntax:** python
**Generated:** 2026-01-03 17:24:45

```python
"""
User interaction utilities for doc-gen.
"""

def prompt_file_selection(filepath, relative_to=None):
    """
    Prompt user to include/exclude a file.
    
    Args:
        filepath: Path object or string to prompt about
        relative_to: Optional Path to show relative path from
        
    Returns:
        bool: True if user wants to include file, False otherwise
    """
    # Show relative path if base provided, otherwise show as-is
    if relative_to:
        from pathlib import Path
        try:
            display_path = Path(filepath).relative_to(relative_to)
        except ValueError:
            display_path = filepath
    else:
        display_path = filepath
    
    # Prompt with default = Yes
    while True:
        response = input(f"[{display_path}] (Y/n)? ").strip().lower()
        
        # Empty or 'y' = yes
        if response in ('', 'y', 'yes'):
            return True
        
        # 'n' = no
        if response in ('n', 'no'):
            return False
        
        # Invalid input, try again
        print("Please enter Y or n")
```
