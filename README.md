# Doc-Gen: Documentation Generator

A Python tool that automatically generates syntax-highlighted markdown documentation from your project files. Designed to be simple, reusable, and Ansible-friendly.

## What It Does

Doc-Gen mirrors your project directory structure and creates markdown files with syntax-highlighted code blocks from your source files. Perfect for:

- Documenting deployment scripts and configurations
- Creating readable archives of codebases
- Generating documentation for BookStack or other wiki systems
- Maintaining up-to-date project documentation

## Origin Story

Born from frustration with manually copying 20+ deployment scripts into BookStack. What took 30+ minutes of fighting with clipboard and UI automation now takes 2 seconds.

The "Doors of Durin" philosophy: **Simple automation beats complex UIs**.

## Key Features

- **Two-phase workflow**: Interactive selection + repeatable generation
- **Respects .gitignore**: Uses existing exclusion patterns (DRY principle)
- **YAML configuration**: Easy to read, edit, and version control
- **Manifest-based**: Clear audit trail of what's documented
- **Automatic backups**: Timestamped manifest backups
- **Check mode**: Dry-run to preview what would be generated
- **Plugin-ready architecture**: Extensible for custom formats (future)
- **Project tree generation**: Visual directory structue with optional gitignored files
## Requirements

- Python 3.8 or higher
- PyYAML (`pip install pyyaml`)
- pathspec (`pip install pathspec`)

## Installation
````bash
# Clone the repository
git clone [your-repo-url] doc-gen
cd doc-gen

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install pyyaml pathspec

# Create configuration file
python -m doc_gen.ui.menu
# Select: 4. Initialize Config
````

## Quick Start

### 1. Initialize Configuration
````bash
python -m doc_gen.ui.menu
````

Select option 4 to create `doc-config.yml` from template.

### 2. Interactive Mode - Select Files

Navigate to your project and run Interactive Mode to build a manifest:
````bash
python -m doc_gen.ui.menu
# Select: 1. Interactive Mode
# Enter project directory (or press Enter for current directory)
# Answer Y/n for each file
````

This creates `manifest.yml` listing your selected files.

### 3. Generate Documentation
````bash
python -m doc_gen.ui.menu
# Select: 2. Generate Documentation
# Press Enter to use manifest.yml
````

Your markdown files are now in `docs/mirror/` (or configured output directory)!

### 4. Check Before Generating (Optional)

Preview what would be generated without writing files:
````bash
python -m doc_gen.ui.menu
# Select: 3. Check Mode
````

## Configuration

Edit `doc-config.yml` to customize behavior:
````yaml
project:
  root: "."                    # Project root directory
  gitignore: ".gitignore"      # Path to .gitignore file

output:
  base_dir: "docs/mirror"      # Where to create documentation
  manifest_file: "manifest.yml" # Manifest filename
  format: "yaml"               # Manifest format

syntax_map:
  # Map file extensions to syntax highlighting
  .sh: bash
  .py: python
  .yml: yaml
  .yaml: yaml
  .container: ini
  .service: ini
  .md: markdown
  .txt: text
  .json: json
  .toml: toml
  # Add your own mappings here

exclusions:
  # Additional patterns beyond .gitignore
  - "*.pyc"
  - "__pycache__"
  - "*.log"
  - ".DS_Store"
````

## Menu Options

**Main Menu:**
1. **Interactive Mode** - Scan project and build manifest
2. **Generate Documentation** - Create markdown from manifest
3. **Check Mode** - Dry-run preview with file export
4. **Initialize Config** - Create configuration template
5. **Settings** - View/edit configuration and plugins
6. **Exit**

**Settings Menu:**
1. **View Current Configuration** - Display config (paginated)
2. **Edit Configuration Path** - Use different config file
3. **View Plugin Status** - Check loaded plugins
4. **Back to Main Menu**

## Workflow Examples

### Generate Project Tree

Create a visual representation of your project structure:
```bash
python -m doc_gen.ui.menu
# Select: 6. Generate Project Tree
# Optionally include .gitignore patterns (like .env files)
# Save as PROJECT_STRUCTURE.txt
```

Example output:
```
doc-gen/
├── doc_gen/
│   ├── __init__.py
│   ├── core/
│   │   ├── builder.py
│   │   ├── scanner.py
│   │   └── manifest.py
│   └── ui/
│       ├── menu.py
│       └── menu_actions.py
├── .env
├── README.md
└── manifest.yml
```
### Document a New Project
````bash
cd ~/projects/my-app
python -m doc_gen.ui.menu

# 1. Interactive Mode
#    - Prompts for each file
#    - Creates manifest.yml

# 2. Generate Documentation
#    - Reads manifest.yml
#    - Creates docs/mirror/ with markdown files
````


### Update Existing Documentation
````bash
# Files changed? Just regenerate from existing manifest
python -m doc_gen.ui.menu
# Select: 2. Generate Documentation

# Need to add/remove files? Run Interactive Mode again
# (Old manifest automatically backed up with timestamp)
````

### Preview Changes (Check Mode)
````bash
python -m doc_gen.ui.menu
# Select: 3. Check Mode
# Review what would be generated
# Optionally save report to file
````

## Generated Output Format

Each markdown file includes:
````markdown
# filename.py

**Path:** relative/path/to/file.py
**Syntax:** python
**Generated:** 2026-01-03 12:34:56
```python
# Full file contents here
# with syntax highlighting
```
````

Directory structure mirrors source:
````
docs/mirror/
├── scripts/
│   ├── deploy.sh.md
│   └── configure.sh.md
├── configs/
│   └── app.yml.md
└── README.md.md
````

## Windows Compatibility

Doc-Gen works on Windows! Tips:

- Use forward slashes in config paths: `docs/mirror` (not `docs\mirror`)
- Activate virtual environment: `.venv\Scripts\activate`
- Git Bash or WSL recommended but not required
- Pagination uses `more` instead of `less`

## Design Philosophy

### Two-Phase Workflow

1. **Interactive Mode** (human control)
   - Review and approve files
   - Build manifest
   
2. **Unattended Mode** (automation)
   - Generate from manifest
   - Repeatable, idempotent

### Why Manifests?

- **Audit trail**: See exactly what's documented
- **Version control**: Track manifest changes over time
- **Repeatability**: Generate docs consistently
- **CI/CD friendly**: Automated documentation updates

### Why YAML?

- Human-readable
- Easy to edit manually
- Version control friendly
- Ansible ecosystem compatible

## Troubleshooting

### No files found during scan

Check your `.gitignore` - you might be excluding everything!

### Wrong output directory

Check `output.base_dir` in `doc-config.yml`

### Missing syntax highlighting

Add the file extension to `syntax_map` in config

### Manifest has 0 files

This was a bug in early versions - make sure you're using the latest `manifest.py`

## Future Enhancements

- [ ] CLI arguments (alternative to menu)
- [ ] Diff mode (show changes since last generation)
- [ ] Watch mode (auto-regenerate on file changes)
- [ ] Custom templates
- [ ] HTML/PDF output formats
- [ ] Direct BookStack API integration
- [ ] Metadata extraction from docstrings

## Development

### Project Structure
````
doc-gen/
├── doc_gen/              # Main package
│   ├── core/            # Core functionality
│   ├── ui/              # User interface (menu, CLI)
│   ├── plugins/         # Plugin system
│   └── utils/           # Utilities
├── examples/            # Example projects
├── tests/               # Unit tests
└── doc-config.yml       # Your configuration
````

### Running Tests
````bash
# Not yet implemented - contributions welcome!
pytest tests/
````

## Contributing

Contributions welcome! Areas of interest:

- Additional syntax mappings
- Output format plugins (HTML, PDF)
- Better error messages
- Unit tests
- Documentation improvements

## License

[Your chosen license]

## Author

[Your name/info]

## Acknowledgments

Created to solve real documentation pain points. Inspired by the principle that 2 seconds of automation beats 30 minutes of manual work.

---

*"The Doors of Durin were simple: speak 'friend' and enter. Good tools should simple to use,too."*