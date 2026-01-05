# generator.py

**Path:** doc_gen/core/generator.py
**Syntax:** python
**Generated:** 2026-01-03 17:24:45

```python
"""
Markdown documentation generator for doc-gen.
Reads manifest and generates syntax-highlighted markdown files.
"""

from pathlib import Path
from datetime import datetime
from doc_gen.core.manifest import read_manifest


class MarkdownGenerator:
    """
    Generate markdown documentation from manifest.
    
    Creates mirror directory structure and syntax-highlighted markdown files.
    """
    
    def __init__(self, manifest_path, project_root, output_dir, syntax_map=None):
        """
        Initialize markdown generator.
        
        Args:
            manifest_path: Path to manifest.yml file
            project_root: Root directory of source project
            output_dir: Where to create documentation mirror
            syntax_map: Dict mapping file extensions to syntax names (optional)
        """
        self.manifest_path = Path(manifest_path)
        self.project_root = Path(project_root)
        self.output_dir = Path(output_dir)
        
        # Default syntax mappings
        self.syntax_map = syntax_map or {
            '.sh': 'bash',
            '.py': 'python',
            '.yml': 'yaml',
            '.yaml': 'yaml',
            '.container': 'ini',
            '.network': 'ini',
            '.service': 'ini',
            '.conf': 'bash',
            '.md': 'markdown',
            '.txt': 'text',
            '.json': 'json',
            '.toml': 'toml',
            '.ini': 'ini',
            '.js': 'javascript',
            '.html': 'html',
            '.css': 'css',
            '.xml': 'xml',
        }
        
        # Statistics
        self.stats = {
            'total_files': 0,
            'generated': 0,
            'skipped': 0,
            'errors': 0
        }
    
    def detect_syntax(self, filepath):
        """
        Detect syntax highlighting language from file extension.
        
        Args:
            filepath: Path object
            
        Returns:
            str: Syntax name (e.g., 'python', 'bash') or empty string
        """
        return self.syntax_map.get(filepath.suffix, '')
    
    def generate_markdown_content(self, source_file, relative_path):
        """
        Generate markdown content for a single file.
        
        Args:
            source_file: Path to source file
            relative_path: Relative path from project root
            
        Returns:
            str: Markdown content
        """
        syntax = self.detect_syntax(source_file)
        
        # Read source file
        try:
            content = source_file.read_text(errors='ignore')
        except Exception as e:
            content = f"[Error reading file: {e}]"
        
        # Build markdown
        markdown = f"# {source_file.name}\n\n"
        markdown += f"**Path:** {relative_path}\n"
        markdown += f"**Syntax:** {syntax if syntax else 'text'}\n"
        markdown += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        markdown += f"```{syntax}\n"
        markdown += content
        markdown += "\n```\n"
        
        return markdown
    
    def create_mirror_structure(self, relative_path):
        """
        Create mirror directory structure in output location.
        
        Args:
            relative_path: Relative path of file from project root
            
        Returns:
            Path: Output path for the markdown file
        """
        # Get the directory part of the relative path
        file_path = Path(relative_path)
        
        # Create corresponding directory in output
        if file_path.parent != Path('.'):
            output_subdir = self.output_dir / file_path.parent
            output_subdir.mkdir(parents=True, exist_ok=True)
        
        # Return the full output path with .md extension
        output_file = self.output_dir / f"{relative_path}.md"
        return output_file
    
    def generate_file(self, relative_path):
        """
        Generate markdown documentation for a single file.
        
        Args:
            relative_path: Relative path from project root
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Get source file path
        source_file = self.project_root / relative_path
        
        # Check if source exists
        if not source_file.exists():
            print(f"  ✗ Source not found: {relative_path}")
            self.stats['skipped'] += 1
            return False
        
        # Skip directories
        if source_file.is_dir():
            print(f"  ⊘ Skipping directory: {relative_path}")
            self.stats['skipped'] += 1
            return False
        
        try:
            # Create output path
            output_path = self.create_mirror_structure(relative_path)
            
            # Generate markdown
            markdown = self.generate_markdown_content(source_file, relative_path)
            
            # Write to file
            output_path.write_text(markdown, encoding='utf-8')
            
            print(f"  ✓ Generated: {output_path.relative_to(self.output_dir)}")
            self.stats['generated'] += 1
            return True
            
        except Exception as e:
            print(f"  ✗ Error generating {relative_path}: {e}")
            self.stats['errors'] += 1
            return False
    
    def generate_all(self):
        """
        Generate documentation for all files in manifest.
        
        Returns:
            dict: {'success': bool, 'message': str, 'stats': dict}
        """
        # Read manifest
        manifest_result = read_manifest(self.manifest_path)
        
        if not manifest_result['success']:
            return {
                'success': False,
                'message': manifest_result['message'],
                'stats': self.stats
            }
        
        documents = manifest_result['documents']
        self.stats['total_files'] = len(documents)
        
        if not documents:
            return {
                'success': False,
                'message': 'No files in manifest',
                'stats': self.stats
            }
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\nGenerating documentation...")
        print(f"Source: {self.project_root}")
        print(f"Output: {self.output_dir}")
        print(f"Files: {len(documents)}\n")
        
        # Generate each file
        for doc_path in documents:
            self.generate_file(doc_path)
        
        # Summary
        print(f"\n{'=' * 50}")
        print(f"Generation complete!")
        print(f"  Generated: {self.stats['generated']}")
        print(f"  Skipped:   {self.stats['skipped']}")
        print(f"  Errors:    {self.stats['errors']}")
        print(f"  Total:     {self.stats['total_files']}")
        print('=' * 50)
        
        return {
            'success': True,
            'message': f"Generated {self.stats['generated']} markdown files",
            'stats': self.stats
        }
    
    def print_stats(self):
        """Print generation statistics."""
        print(f"\n=== Generation Statistics ===")
        print(f"Total files:  {self.stats['total_files']}")
        print(f"Generated:    {self.stats['generated']}")
        print(f"Skipped:      {self.stats['skipped']}")
        print(f"Errors:       {self.stats['errors']}")

```
