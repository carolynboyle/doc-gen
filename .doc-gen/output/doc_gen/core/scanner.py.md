# scanner.py

**Path:** doc_gen/core/scanner.py
**Syntax:** python
**Generated:** 2026-03-26 19:01:15

```python
"""
Project directory scanning for doc-gen.
Walks directory tree, respects ignore patterns, 
detects binary files, and collects files for documentation.
"""
import os
from pathlib import Path
from fnmatch import fnmatch
from doc_gen.core.config import IGNORE_PATTERNS_FILE, HARDCODED_IGNORES


class ProjectScanner:
    """
    Scan project directory tree and collect files for documentation.

    Respects ignore patterns from .doc-gen/ignore-patterns.txt, excludes binary files, 
    and applies additional exclusion rules.
    ALWAYS excludes .doc-gen/ directory (hardcoded - tool never documents itself).
    """

    def __init__(self, root_dir, exclusions=None, include_patterns=None):
        """
        Initialize project scanner.

        Args:
            root_dir: Root directory to scan (Path object or string)
            exclusions: Additional glob patterns to exclude (list of strings)
            include_patterns: Ignore patterns to temporarily include (list of strings)
        """
        self.root_dir = Path(root_dir).resolve()

        # Load patterns from centralized ignore-patterns.txt
        self.ignore_patterns = self._load_ignore_patterns()

        # Remove patterns user wants to include for documentation
        if include_patterns:
            self.ignore_patterns = [p for p in self.ignore_patterns
            if p not in include_patterns]

        # ALWAYS enforce hardcoded exclusions (can never be removed)
        self.ignore_patterns.extend(HARDCODED_IGNORES)

        # Additional exclusion patterns (globs) - optional override
        if exclusions:
            self.ignore_patterns.extend(exclusions)

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

    def _load_ignore_patterns(self):
        """Load patterns from .doc-gen/ignore-patterns.txt"""
        if not IGNORE_PATTERNS_FILE.exists():
            return []

        patterns = []
        for line in IGNORE_PATTERNS_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith('#'):
                patterns.append(line)

        return patterns

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

    def _matches_pattern(self, path):
        """
        Check if path matches any ignore pattern.

        Args:
            path: Path to check (Path object)

        Returns:
            bool: True if path matches any ignore pattern
        """
        for pattern in self.ignore_patterns:
            # Directory pattern (ends with /)
            if pattern.endswith('/'):
                dir_name = pattern.rstrip('/')
                # Check if this directory name appears anywhere in the path
                if dir_name in path.parts:
                    return True
            # File glob pattern
            elif fnmatch(path.name, pattern):
                return True
        return False

    def _should_skip_dir(self, dir_path):
        """
        Check if directory should be skipped.

        Args:
            dir_path: Directory path (Path object)

        Returns:
            bool: True if directory should be skipped
        """
        # HARDCODED: Always skip .doc-gen directory (redundant check, but explicit)
        if '.doc-gen' in dir_path.parts:
            return True

        # Get relative path for pattern matching
        try:
            rel_path = dir_path.relative_to(self.root_dir)
        except ValueError:
            # Path not relative to root
            return True

        # Check ignore patterns
        if self._matches_pattern(rel_path):
            return True

        return False

    def _should_skip_file(self, file_path):
        """
        Check if file should be skipped.

        Args:
            file_path: File path (Path object)

        Returns:
            tuple: (should_skip: bool, reason: str)
        """
        # HARDCODED: Always skip files in .doc-gen directory (redundant, but explicit)
        if '.doc-gen' in file_path.parts:
            return (True, 'doc-gen')

        # Get relative path for pattern matching
        try:
            rel_path = file_path.relative_to(self.root_dir)
        except ValueError:
            return (True, 'not_in_project')

        # Check ignore patterns
        if self._matches_pattern(rel_path):
            return (True, 'ignored')

        # Check if binary file
        if self._is_binary_file(file_path):
            # Track for reporting
            self.binary_files.append(rel_path)
            return (True, 'binary')

        return (False, 'included')

    def scan_files(self):
        """
        Walk the project directory and collect files for documentation.

        Uses os.walk with in-place directory pruning so ignored directories
        are never descended into. Resets stats and binary file tracking on
        each call, so the same scanner instance can be reused safely.

        Returns:
            list: Relative Path objects for collected files, sorted alphabetically.
        """
        collected_files = []
        self.binary_files = []
        self.stats = {
            'total_files': 0,
            'ignored_files': 0,
            'excluded_files': 0,
            'binary_files': 0,
            'collected_files': 0
        }

        for dirpath, dirnames, filenames in os.walk(self.root_dir):
            current_dir = Path(dirpath)

            # Prune ignored directories IN PLACE so os.walk won't descend
            dirnames[:] = [
                d for d in dirnames
                if not self._should_skip_dir(current_dir / d)
            ]

            for filename in filenames:
                file_path = current_dir / filename
                self.stats['total_files'] += 1

                should_skip, reason = self._should_skip_file(file_path)

                if should_skip:
                    if reason == 'ignored':
                        self.stats['ignored_files'] += 1
                    elif reason == 'binary':
                        self.stats['binary_files'] += 1
                else:
                    rel_path = file_path.relative_to(self.root_dir)
                    collected_files.append(rel_path)
                    self.stats['collected_files'] += 1

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
            print("\n  Binary files detected:")
            for bf in self.binary_files[:10]:  # Show first 10
                print(f"    - {bf}")
            if len(self.binary_files) > 10:
                print(f"    ... and {len(self.binary_files) - 10} more")


# Convenience function for quick scans
def quick_scan(root_dir, exclusions=None):
    """
    Quick scan of project directory.

    Args:
        root_dir: Root directory to scan
        exclusions: Additional exclusion patterns (optional)

    Returns:
        list: Collected file paths
    """
    scanner = ProjectScanner(root_dir, exclusions)
    return scanner.scan_files()
    
```
