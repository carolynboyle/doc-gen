# Output Format

Understanding doc-gen's output structure and generated files.

## Output Directory Structure

All doc-gen output lives in `.doc-gen/`:

```
.doc-gen/
├── config.yml              # Configuration settings
├── manifest.yml            # Selected files list
├── ignore-patterns.txt     # File exclusion patterns
├── project-tree.txt        # Generated project tree
├── docs/                   # Generated markdown documentation
│   ├── src/
│   │   ├── main.py.md
│   │   └── utils.py.md
│   └── scripts/
│       └── deploy.sh.md
└── backups/                # Timestamped backups
    ├── manifest-2025-01-07-14-30-00.yml
    └── ignore-patterns-2025-01-06-10-15-00.txt
```

## Generated Markdown Files

### Directory Mirroring

doc-gen mirrors your project structure:

**Your project:**
```
myproject/
├── src/
│   ├── main.py
│   └── utils.py
└── scripts/
    └── deploy.sh
```

**Generated docs:**
```
.doc-gen/docs/
├── src/
│   ├── main.py.md
│   └── utils.py.md
└── scripts/
    └── deploy.sh.md
```

Notice `.md` is appended to preserve the original filename.

### Individual File Format

Each generated markdown file follows this structure:

```markdown
# filename.ext

**Path:** relative/path/from/project/root
**Syntax:** detected-language
**Generated:** 2025-01-07 14:30:00

```language
[complete file contents]
```
```

**Example (Python file):**

```markdown
# main.py

**Path:** src/main.py
**Syntax:** python
**Generated:** 2025-01-07 14:30:00

```python
#!/usr/bin/env python3
"""Main application entry point."""

def main():
    print("Hello, world!")

if __name__ == "__main__":
    main()
```
```

### Syntax Highlighting

Syntax is detected from file extension using your configuration's `syntax_map`. Common examples:

- `.py` → `python`
- `.sh` → `bash`
- `.js` → `javascript`
- `.yml` → `yaml`
- `.md` → `markdown`
- `.txt` → `text` (no highlighting)

The syntax name determines how code is highlighted when viewed in markdown renderers (GitHub, BookStack, etc.).

## Manifest Format

The manifest (`.doc-gen/manifest.yml`) is a human-readable YAML file:

```yaml
# Generated: 2025-01-07 14:25:00
# doc-gen manifest - selected files for documentation
files:
  - path: src/main.py
    syntax: python
  - path: src/utils.py
    syntax: python
  - path: scripts/deploy.sh
    syntax: bash
  - path: README.md
    syntax: markdown
```

**Fields:**
- `path` - Relative path from project root
- `syntax` - Language for syntax highlighting

**Notes:**
- Can be manually edited (useful for fixing syntax assignments)
- Automatically backed up before replacement
- Comments are preserved
- Order is preserved

## Project Tree Format

The project tree (`.doc-gen/project-tree.txt`) uses standard tree formatting:

```
myproject/
├── src/
│   ├── __init__.py
│   ├── main.py
│   └── utils.py
├── scripts/
│   └── deploy.sh
├── tests/
│   └── test_main.py
├── README.md
└── setup.py
```

**Characteristics:**
- Respects ignore patterns
- Excludes binary files
- Shows directory structure only (no file contents)
- Uses standard tree symbols (├──, └──, │)

## Configuration Format

Configuration (`.doc-gen/config.yml`) uses YAML:

```yaml
project:
  root: "."
  
output:
  base_dir: ".doc-gen/docs"
  manifest_file: ".doc-gen/manifest.yml"
  
syntax_map:
  .py: python
  .sh: bash
  # ... more mappings
```

See [Configuration](configuration.md) for full details.

## Ignore Patterns Format

Ignore patterns (`.doc-gen/ignore-patterns.txt`) use gitignore syntax:

```
# Comments start with #
*.pyc
*.log
__pycache__/
.venv/
node_modules/
*.swp
.DS_Store
```

**Rules:**
- One pattern per line
- `#` for comments
- `*` for wildcards
- Trailing `/` for directories
- Leading `/` for root-relative paths

## Backup Format

Backups use timestamps in their filenames:

```
manifest-YYYY-MM-DD-HH-MM-SS.yml
ignore-patterns-YYYY-MM-DD-HH-MM-SS.txt
```

**Example:**
```
manifest-2025-01-07-14-30-00.yml
```

Backups are never automatically deleted, so you can recover old configurations.

## Using Generated Documentation

### In GitHub

Generated markdown files render with syntax highlighting automatically:

```markdown
```python
def hello():
    print("World")
```
```

### In BookStack

Import markdown files directly. BookStack supports:
- Syntax highlighting
- Inline code blocks
- Headers and formatting

### In Wikis

Most wiki systems (Confluence, GitLab Wiki, etc.) support standard markdown with code blocks.

### As Plain Text

Markdown is readable even without rendering:

```
# main.py

**Path:** src/main.py
**Syntax:** python

```python
def main():
    print("Hello")
```
```

## Tips

- **Keep `.doc-gen/` in .gitignore** - Don't commit generated docs unless intentional
- **Commit manifest** - Version control your file selections
- **Share tree files** - Great for documentation without revealing code
- **Manual edits** - Manifest and config are YAML, safe to edit by hand

## Next Steps

- Learn about [Configuration](configuration.md) to customize output
- See [Workflows](workflows.md) for generating documentation
- Check [Troubleshooting](troubleshooting.md) if output isn't as expected
