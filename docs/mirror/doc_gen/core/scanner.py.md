# scanner.py

**Path:** doc_gen/core/scanner.py
**Syntax:** python
**Generated:** 2026-01-03 17:24:45

```python
''' ProjectScanner: Walks directory tree  '''
"""
Project directory scanning for doc-gen.
Walks directory tree, respects .gitignore, and collects files for documentation.
"""

from pathlib import Path
from fnmatch import fnmatch
from doc_gen.core.gitignore import GitignoreParser


class ProjectScanner:
    """
    Scan project directory tree and collect files for documentation.
    
    Respects .gitignore patterns and additional exclusion rules.
    """
    
    def __init__(self, root_dir, gitignore_path=None, exclusions=None):
        """
        Initialize project scanner.
        
        Args:
            root_dir: Root directory to scan (Path object or string)
            gitignore_path: Path to .gitignore file (default: root_dir/.gitignore)
            exclusions: Additional glob patterns to exclude (list of strings)
        """
        self.root_dir = Path(root_dir).resolve()
        
        # Set up gitignore parser
        if gitignore_path is None:
            gitignore_path = self.root_dir / '.gitignore'
        self.gitignore = GitignoreParser(gitignore_path)
        
        # Additional exclusion patterns (globs)
        self.exclusions = exclusions or []
        
        # Statistics
        self.stats = {
            'total_files': 0,
            'ignored_files': 0,
            'excluded_files': 0,
            'collected_files': 0
        }
    
    def _matches_exclusion(self, path):
        """
        Check if path matches any additional exclusion pattern.
        
        Args:
            path: Path to check (Path object)
            
        Returns:
            bool: True if path matches exclusion pattern
        """
        for pattern in self.exclusions:
            if fnmatch(path.name, pattern):
                return True
        return False
    
    def _should_skip_dir(self, dir_path):
        """
        Check if directory should be skipped.
        
        Args:
            dir_path: Directory path relative to root (Path object)
            
        Returns:
            bool: True if directory should be skipped
        """
        # Get relative path for gitignore matching
        try:
            rel_path = dir_path.relative_to(self.root_dir)
        except ValueError:
            # Path not relative to root
            return True
        
        # Check gitignore patterns
        if self.gitignore.should_ignore(rel_path, is_dir=True):
            return True
        
        # Check additional exclusions
        if self._matches_exclusion(dir_path):
            return True
        
        return False
    
    def _should_skip_file(self, file_path):
        """
        Check if file should be skipped.
        
        Args:
            file_path: File path relative to root (Path object)
            
        Returns:
            tuple: (should_skip: bool, reason: str)
        """
        # Get relative path for gitignore matching
        try:
            rel_path = file_path.relative_to(self.root_dir)
        except ValueError:
            return (True, 'not_in_project')
        
        # Check gitignore patterns
        if self.gitignore.should_ignore(rel_path, is_dir=False):
            return (True, 'gitignore')
        
        # Check additional exclusions
        if self._matches_exclusion(file_path):
            return (True, 'exclusion')
        
        return (False, 'included')
    
    def scan_files(self):
        """
        Scan project directory and collect files for documentation.
        
        Returns:
            list: List of Path objects (relative to root_dir) for files to document
        """
        collected_files = []
        
        # Reset statistics
        self.stats = {
            'total_files': 0,
            'ignored_files': 0,
            'excluded_files': 0,
            'collected_files': 0
        }
        
        # Walk the directory tree
        for item in self.root_dir.rglob('*'):
            # Skip directories themselves (we only want files)
            if item.is_dir():
                # But check if we should skip this directory's contents
                if self._should_skip_dir(item):
                    # Note: rglob will still descend, but we filter files
                    continue
            
            # Process files only
            if item.is_file():
                self.stats['total_files'] += 1
                
                should_skip, reason = self._should_skip_file(item)
                
                if should_skip:
                    if reason == 'gitignore':
                        self.stats['ignored_files'] += 1
                    elif reason == 'exclusion':
                        self.stats['excluded_files'] += 1
                else:
                    # Get path relative to root for consistent output
                    rel_path = item.relative_to(self.root_dir)
                    collected_files.append(rel_path)
                    self.stats['collected_files'] += 1
        
        # Sort files for consistent ordering
        collected_files.sort()
        
        return collected_files
    
    def get_stats(self):
        """
        Get scanning statistics.
        
        Returns:
            dict: Statistics about the scan (total, ignored, excluded, collected)
        """
        return self.stats.copy()
    
    def print_stats(self):
        """Print scanning statistics in a readable format."""
        print("\nScan Statistics:")
        print(f"  Total files found:    {self.stats['total_files']}")
        print(f"  Gitignore filtered:   {self.stats['ignored_files']}")
        print(f"  Exclusion filtered:   {self.stats['excluded_files']}")
        print(f"  Files to document:    {self.stats['collected_files']}")


# Convenience function for quick scans
def quick_scan(root_dir, gitignore_path=None, exclusions=None):
    """
    Quick scan of project directory.
    
    Args:
        root_dir: Root directory to scan
        gitignore_path: Path to .gitignore file
        exclusions: Additional exclusion patterns
        
    Returns:
        list: Collected file paths
    """
    scanner = ProjectScanner(root_dir, gitignore_path, exclusions)
    return scanner.scan_files()

```
