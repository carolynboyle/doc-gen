# doc-config.yml

**Path:** doc-config.yml
**Syntax:** yaml
**Generated:** 2026-01-03 17:24:45

```yaml
# Doc-Gen Configuration Template
# Copy this to doc-config.yml and customize for your project

project:
  # Root directory to scan (relative to where doc-gen runs)
  root: "."
  
  # Path to .gitignore file to respect (relative to root)
  # Set to null or "" to disable gitignore parsing
  gitignore: ".gitignore"

output:
  # Base directory for generated documentation
  base_dir: "docs/mirror"
  
  # Manifest file path (relative to current directory)
  manifest_file: "manifest.yml"
  
  # Manifest format (currently only yaml supported)
  format: "yaml"

# File extension to syntax highlighting mapping
syntax_map:
  # Shell scripts
  .sh: bash
  .bash: bash
  
  # Python
  .py: python
  
  # YAML/Config files
  .yml: yaml
  .yaml: yaml
  .toml: toml
  .ini: ini
  .conf: bash
  
  # Systemd/Podman quadlets
  .container: ini
  .volume: ini
  .network: ini
  .service: ini
  
  # Documentation
  .md: markdown
  .txt: text
  .rst: rst
  
  # Web/Data
  .html: html
  .css: css
  .js: javascript
  .json: json
  .xml: xml
  
  # Other common types
  .sql: sql
  .env: bash

# Additional exclusion patterns beyond .gitignore
# These are applied even if no .gitignore exists
exclusions:
  # Python artifacts
  - "*.pyc"
  - "*.pyo"
  - "__pycache__"
  - "*.egg-info"
  - ".pytest_cache"
  - "venv"
  - ".venv"
  
  # System files
  - ".DS_Store"
  - "Thumbs.db"
  - "desktop.ini"
  
  # Logs and databases
  - "*.log"
  - "*.sqlite"
  - "*.db"
  
  # IDE and editor files
  - ".idea"
  - ".vscode"
  - "*.swp"
  - "*.swo"
  - "*~"
  
  # Version control
  - ".git"
  - ".svn"
  
  # Generated documentation (avoid recursion)
  - "docs/mirror"

# Plugin settings (optional)
plugins:
  # Enable/disable plugin types
  enabled:
    syntax_detection: true
    formatters: true
    processors: true
  
  # Plugin directories to search (relative to doc-gen installation)
  search_paths:
    - "plugins"
    - "~/.doc-gen/plugins"

# Logging configuration
logging:
  # Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
  level: "INFO"
  
  # Log file path (null for console only)
  file: null
  
  # Log format
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

```
