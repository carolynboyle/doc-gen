# menu-reference.md

**Path:** docs/menu-reference.md
**Syntax:** markdown
**Generated:** 2026-03-26 19:01:15

```markdown
# Menu Reference

Complete reference for all doc-gen menu options.

## Main Menu

```
╔════════════════════════════════════════════════════════════╗
║                   DOC-GEN MAIN MENU                        ║
╚════════════════════════════════════════════════════════════╝

1. Generate Project Tree
2. Scan Project - Select files to document
3. Check Mode - Review selected files (paginated)
4. Generate Documentation
5. Settings
6. Exit
```

### Option 1: Generate Project Tree

**Purpose:** Creates a visual tree of your project structure.

**What it does:**
- Recursively scans your project directory
- Respects ignore patterns (`.gitignore` and `.doc-gen/ignore-patterns.txt`)
- Shows directory structure with tree formatting
- Saves to `.doc-gen/project-tree.txt`

**When to use:**
- Before scanning, to see what's in your project
- To verify ignore patterns are working correctly
- To share your project structure without revealing code

**Notes:**
- This is independent of file selection (no manifest needed)
- Always excludes `.doc-gen/`, `.git/`, and `__pycache__/`
- Automatically detects and skips binary files

### Option 2: Scan Project - Select Files to Document

**Purpose:** Interactively choose which files to include in documentation.

**What it does:**
- Scans project respecting ignore patterns
- Presents each file for approval
- Saves selections to `.doc-gen/manifest.yml`
- Backs up previous manifest (if exists) with timestamp

**Interactive prompts:**

```
File 1 of 42: src/main.py
[A]ccept  [S]kip  [Q]uit  [T]oggle auto-accept  [?] = Help

Choice:
```

**Controls:**
- `A` or `a` - Accept this file (add to manifest)
- `S` or `s` - Skip this file
- `Q` or `q` - Quit and save manifest with current selections
- `T` or `t` - Toggle auto-accept mode (accepts all remaining files)
- `?` - Show help

**Auto-accept mode:**
When toggled, automatically accepts all remaining files without prompting. Toggle again to go back to manual mode.

**Notes:**
- Binary files are automatically skipped
- Previous manifest is backed up before replacement
- Manifest can be manually edited (it's just YAML)
- Can re-run to update file selection

### Option 3: Check Mode - Review Selected Files

**Purpose:** Preview what will be documented before generating.

**What it does:**
- Reads `.doc-gen/manifest.yml`
- Displays all selected files with details
- Shows file sizes and syntax highlighting
- Paginates output for easy reading

**Display format:**

```
Selected Files (15 total):

1. src/main.py (2.3 KB) - python
2. src/utils.py (1.1 KB) - python
3. scripts/deploy.sh (856 B) - bash
...

[Press Enter for more, or 'q' to quit]
```

**When to use:**
- Before generating documentation
- To verify file selection
- To check syntax highlighting assignments
- To see total number of files

**Notes:**
- Requires manifest to exist (run Scan Project first)
- Non-destructive (just viewing, no changes made)
- Automatically paginates for long lists

### Option 4: Generate Documentation

**Purpose:** Create markdown documentation files from manifest.

**What it does:**
- Reads `.doc-gen/manifest.yml`
- Creates `.doc-gen/docs/` directory structure
- Mirrors your project's directory layout
- Generates syntax-highlighted markdown for each file
- Shows progress bar during generation

**Output structure:**

```
.doc-gen/docs/
├── src/
│   ├── main.py.md
│   └── utils.py.md
├── scripts/
│   └── deploy.sh.md
└── README.md.md
```

**Generated markdown format:**

```markdown
# filename.ext

**Path:** relative/path/to/file
**Syntax:** language
**Generated:** 2025-01-07 14:30:00

```language
[file contents with syntax highlighting]
```
```

**When to use:**
- After selecting files (Option 2)
- When source files have changed (regenerate)
- To update documentation

**Notes:**
- Requires manifest to exist
- Overwrites existing docs in `.doc-gen/docs/`
- Creates directories as needed
- Skips binary files automatically

### Option 5: Settings

**Purpose:** Configure doc-gen behavior and view settings.

**Settings submenu:**

```
Settings Menu:

1. View Current Configuration
2. Edit Configuration Path
3. Manage Ignore Patterns
4. Return to Main Menu
```

#### 5.1: View Current Configuration

Shows your active configuration:

```yaml
Configuration loaded from: .doc-gen/config.yml

project:
  root: "."
  
output:
  base_dir: ".doc-gen/docs"
  manifest_file: ".doc-gen/manifest.yml"
  
syntax_map:
  .py: python
  .sh: bash
  ...
```

#### 5.2: Edit Configuration Path

Change which config file doc-gen uses:

```
Current config path: .doc-gen/config.yml
Enter new config path (or press Enter to keep current):
```

Useful for:
- Project-specific configurations
- Testing different settings
- Using shared config files

#### 5.3: Manage Ignore Patterns

Submenu for managing file exclusions:

```
Manage Ignore Patterns:

1. View Current Patterns
2. Edit Patterns (opens in editor)
3. Reset to Defaults
4. Return to Settings Menu
```

**View Patterns:**
Shows numbered list of active ignore patterns.

**Edit Patterns:**
Opens `.doc-gen/ignore-patterns.txt` in your default editor.

**Reset to Defaults:**
Restores ignore patterns to defaults. Current patterns are backed up with timestamp.

### Option 6: Exit

**Purpose:** Quit doc-gen.

Exits cleanly. All state is saved in `.doc-gen/` directory.

## Keyboard Shortcuts

None currently implemented, but numbered menu selections work throughout:

- Type number + Enter to select
- Most prompts accept single letter responses (case insensitive)

## Tips

- **Menu is context-aware** - Options only appear when relevant
- **No wrong turns** - You can always return to main menu
- **State is preserved** - Your selections survive crashes/exits
- **Help is available** - Press `?` during file selection for help

## Next Steps

- See [Workflows](workflows.md) for step-by-step usage
- Check [Configuration](configuration.md) for customization options
- Review [Output Format](output-format.md) for generated file structure

```
