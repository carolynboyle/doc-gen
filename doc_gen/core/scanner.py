"""
Project directory scanning for doc-gen.
Walks directory tree, respects .gitignore, detects binary files, and collects files for documentation.
"""

from pathlib import Path
from fnmatch import fnmatch
from doc_gen.core.gitignore import GitignoreParser


class ProjectScanner:
    """
    Scan project directory tree and collect files for documentation.

    Respects .gitignore patterns, excludes binary files, and applies additional exclusion rules.
    ALWAYS excludes .doc-gen/ directory (hardcoded - tool never documents itself).
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

        # Track binary files for reporting
        self.binary_files = []

        # Statistics
        self.stats = {
            'total_files': 0,
            'ignored_files': 0,
            'excluded_files': 0,
            'binary_files': 0,
            'collected_files': 0
        }

    def _is_binary_file(self, file_path):
        """
        Check if file is binary (non-text).
        
        Args:
            file_path: Path to check
            
        Returns:
            bool: True if binary file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                # Try reading first 512 bytes as text
                f.read(512)
            return False
        except (UnicodeDecodeError, IOError):
            return True  # Binary or unreadable

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
        # HARDCODED: Always skip .doc-gen directory
        if '.doc-gen' in dir_path.parts:
            return True

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
        # HARDCODED: Always skip files in .doc-gen directory
        if '.doc-gen' in file_path.parts:
            return (True, 'doc-gen')

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

        # Check if binary file
        if self._is_binary_file(file_path):
            # Track for reporting
            self.binary_files.append(rel_path)
            return (True, 'binary')

        return (False, 'included')

    def scan_files(self):
        """
        Scan project directory and collect files for documentation.

        Returns:
            list: List of Path objects (relative to root_dir) for files to document
        """
        collected_files = []

        # Reset statistics and binary file tracking
        self.binary_files = []
        self.stats = {
            'total_files': 0,
            'ignored_files': 0,
            'excluded_files': 0,
            'binary_files': 0,
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
                    elif reason == 'binary':
                        self.stats['binary_files'] += 1
                    # 'doc-gen' and 'not_in_project' don't increment stats
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
            dict: Statistics about the scan (total, ignored, excluded, binary, collected)
        """
        return self.stats.copy()

    def get_binary_files(self):
        """
        Get list of binary files that were skipped.

        Returns:
            list: List of Path objects for binary files
        """
        return self.binary_files.copy()

    def print_stats(self):
        """Print scanning statistics in a readable format."""
        print("\nScan Statistics:")
        print(f"  Total files found:    {self.stats['total_files']}")
        print(f"  Gitignore filtered:   {self.stats['ignored_files']}")
        print(f"  Exclusion filtered:   {self.stats['excluded_files']}")
        print(f"  Binary files skipped: {self.stats['binary_files']}")
        print(f"  Files to document:    {self.stats['collected_files']}")

        # Show binary files if any were found
        if self.binary_files:
            print(f"\n  Binary files detected:")
            for bf in self.binary_files[:10]:  # Show first 10
                print(f"    - {bf}")
            if len(self.binary_files) > 10:
                print(f"    ... and {len(self.binary_files) - 10} more")


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