# configuration.md

**Path:** docs/configuration.md
**Syntax:** markdown
**Generated:** 2026-03-26 19:01:15

```markdown
# Configuration

doc-gen uses YAML configuration files to customize its behavior. Configuration is automatically created in `.doc-gen/config.yml` when you first run doc-gen.

## Configuration File Location

The default location is:

```
.doc-gen/config.yml
```

This keeps all doc-gen files in one place, separate from your project files.

## Configuration Structure

```yaml
project:
  root: "."
  
output:
  base_dir: ".doc-gen/docs"
  manifest_file: ".doc-gen/manifest.yml"
  
syntax_map:
  .py: python
  .sh: bash
  .yml: yaml
  .yaml: yaml
  .js: javascript
  .json: json
  .md: markdown
  .txt: text
  .toml: toml
  .ini: ini
  .conf: bash
  .container: ini
  .network: ini
```

## Configuration Sections

### Project Settings

```yaml
project:
  root: "."
```

- **root** - Project root directory (usually "." for current directory)

### Output Settings

```yaml
output:
  base_dir: ".doc-gen/docs"
  manifest_file: ".doc-gen/manifest.yml"
```

- **base_dir** - Where generated markdown files go
- **manifest_file** - Where file selection list is stored

### Syntax Map

The syntax map tells doc-gen which syntax highlighter to use for each file extension:

```yaml
syntax_map:
  .py: python
  .rb: ruby
  .go: go
```

**Common syntax highlighters:**

- `python` - Python files
- `bash` - Shell scripts, config files
- `javascript` - JavaScript/TypeScript
- `yaml` - YAML configuration
- `json` - JSON data
- `markdown` - Markdown files
- `text` - Plain text (no highlighting)
- `ini` - INI-style config files
- `toml` - TOML configuration
- `c` - C/C++ code
- `java` - Java code
- `rust` - Rust code
- `go` - Go code

### Adding Custom Extensions

To add support for a new file type:

1. Open `.doc-gen/config.yml`
2. Add the extension under `syntax_map:`

```yaml
syntax_map:
  .myext: mylanguage
```

3. Save and run doc-gen normally

## Ignore Patterns

Ignore patterns are stored separately in:

```
.doc-gen/ignore-patterns.txt
```

This file uses gitignore syntax:

```
# Patterns (one per line)
*.pyc
*.log
__pycache__/
.venv/
node_modules/
.DS_Store
```

**Hardcoded exclusions** (always ignored, cannot be removed):
- `.doc-gen/`
- `.git/`
- `__pycache__/`

### Managing Ignore Patterns

From the Settings menu:

```
5. Settings
   3. Manage Ignore Patterns
      1. View Current Patterns
      2. Edit Patterns (opens in editor)
      3. Reset to Defaults
```

When you reset to defaults, your current file is backed up to `.doc-gen/backups/`.

## Viewing Current Configuration

From the main menu:

```
5. Settings
   1. View Current Configuration
```

This shows your active configuration with all current values.

## Changing Configuration Path

If you want to use a different config file:

```
5. Settings
   2. Edit Configuration Path
```

Enter the path to your alternative config file. This is useful if you want project-specific configurations.

## Configuration Tips

- **Keep it simple** - The defaults work well for most projects
- **Back up before editing** - Config is automatically backed up, but manual backups don't hurt
- **Test changes** - Run a scan after changing config to verify it works as expected
- **Use comments** - YAML supports `#` comments

## Troubleshooting

### Config Changes Not Taking Effect

1. Verify the config file path (Settings → View Current Configuration)
2. Check for YAML syntax errors (indentation is critical)
3. Restart doc-gen
4. Try resetting to defaults if all else fails

### Unknown Syntax Highlighter

If a file shows as plain text instead of highlighted:

1. Check that the extension is in `syntax_map`
2. Verify the syntax name is valid (common names listed above)
3. Add the extension if missing

## Next Steps

- Learn about [Menu Reference](menu-reference.md) for detailed menu options
- See [Output Format](output-format.md) for how config affects generated files
- Check [Troubleshooting](troubleshooting.md) for configuration issues

```
