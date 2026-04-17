# README.md

**Path:** README.md
**Syntax:** markdown
**Generated:** 2026-03-26 19:01:15

```markdown
# doc-gen

A Python documentation generator that creates syntax-highlighted markdown files from your project source code. Built with a menu-driven interface and designed to respect your existing project structure.

## What It Does

doc-gen scans your project, lets you select which files to document, and generates clean markdown files with syntax highlighting. Perfect for creating documentation to share in wikis, GitHub, or anywhere else that supports markdown.

## Quick Start

```bash
# Install
pip install -e .

# Run
cd your-project
doc-gen

# Follow the menu:
# 1. Generate Project Tree (optional - see what's in your project)
# 2. Scan Project (select files to document)
# 3. Check Mode (preview what will be generated)
# 4. Generate Documentation (create the markdown files)
```

Output lands in `.doc-gen/docs/` with a mirrored directory structure.

## Key Features

- **Menu-driven interface** - No memorizing commands, just follow the prompts
- **Respects .gitignore** - Automatically excludes files you don't want
- **Syntax highlighting** - Auto-detects language from file extension
- **Non-destructive** - All output in `.doc-gen/` directory, never touches your source
- **Plugin system** - Extend with custom syntax detectors and formatters
- **Timestamped backups** - Automatically backs up your file selection manifest

## Documentation

- **[Installation](docs/installation.md)** - Setup and requirements
- **[Workflows](docs/workflows.md)** - How to use doc-gen step-by-step
- **[Configuration](docs/configuration.md)** - Customize behavior via YAML
- **[Menu Reference](docs/menu-reference.md)** - What each menu option does
- **[Output Format](docs/output-format.md)** - Understanding generated files
- **[Design Philosophy](docs/design-philosophy.md)** - Why it works this way
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues and solutions
- **[Roadmap](docs/roadmap.md)** - Future enhancements
- **[Contributing](docs/contributing.md)** - How to help improve doc-gen

## Project Status

Currently functional with core features implemented. Built as a learning project and shared for class feedback. Feedback welcome via GitHub issues!

## License

MIT License - See [LICENSE](LICENSE) file for details

## Author

Built by someone learning Python with 40 years of programming experience in other languages. This represents both a practical utility and a learning exercise in Python development patterns.

```
