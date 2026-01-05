# gitignore.py

**Path:** doc_gen/core/gitignore.py
**Syntax:** python
**Generated:** 2026-01-03 17:24:45

```python
"""
Gitignore pattern parsing and matching for doc-gen.
Handles .gitignore file parsing and path filtering.
"""

from pathlib import Path
import pathspec


class GitignoreParser:
    """
    Parse and apply .gitignore patterns to filter files and directories.
    
    Uses pathspec library for robust gitignore pattern matching.
    """
    
    def __init__(self, gitignore_path=None):
        """
        Initialize gitignore parser.
        
        Args:
            gitignore_path: Path to .gitignore file (Path object or string)
                           If None, no patterns will be loaded
        """
        self.gitignore_path = Path(gitignore_path) if gitignore_path else None
        self.spec = None
        self._load_patterns()
    
    def _load_patterns(self):
        """Load and compile gitignore patterns from file."""
        if not self.gitignore_path or not self.gitignore_path.exists():
            # No gitignore file - create empty spec
            self.spec = pathspec.PathSpec.from_lines('gitwildmatch', [])
            return
        
        try:
            with open(self.gitignore_path, 'r') as f:
                patterns = f.read().splitlines()
            
            # Use gitwildmatch (git's pattern matching style)
            self.spec = pathspec.PathSpec.from_lines('gitwildmatch', patterns)
            
        except Exception as e:
            print(f"Warning: Could not load {self.gitignore_path}: {e}")
            self.spec = pathspec.PathSpec.from_lines('gitwildmatch', [])
    
    def should_ignore(self, path, is_dir=False):
        """
        Check if a path should be ignored based on gitignore patterns.
        
        Args:
            path: Path to check (Path object or string, relative to project root)
            is_dir: True if path is a directory
            
        Returns:
            bool: True if path should be ignored, False otherwise
        """
        if self.spec is None:
            return False
        
        # Convert to string and normalize
        path_str = str(path)
        
        # Add trailing slash for directories (gitignore convention)
        if is_dir and not path_str.endswith('/'):
            path_str = path_str + '/'
        
        # Check if path matches any ignore pattern
        return self.spec.match_file(path_str)
    
    def get_patterns(self):
        """
        Get list of loaded gitignore patterns.
        
        Returns:
            list: Pattern strings from .gitignore file
        """
        if not self.gitignore_path or not self.gitignore_path.exists():
            return []
        
        try:
            with open(self.gitignore_path, 'r') as f:
                # Return non-empty, non-comment lines
                return [
                    line.strip() 
                    for line in f.read().splitlines() 
                    if line.strip() and not line.strip().startswith('#')
                ]
        except Exception:
            return []


# Convenience function for quick checks
def check_gitignore(path, gitignore_path, is_dir=False):
    """
    Quick check if a path should be ignored.
    
    Args:
        path: Path to check
        gitignore_path: Path to .gitignore file
        is_dir: True if path is a directory
        
    Returns:
        bool: True if path should be ignored
    """
    parser = GitignoreParser(gitignore_path)
    return parser.should_ignore(path, is_dir)
```
