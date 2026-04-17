# workflows.md

**Path:** docs/workflows.md
**Syntax:** markdown
**Generated:** 2026-03-26 19:01:15

```markdown
# Workflows

## Basic Workflow

The typical doc-gen workflow has four steps:

1. **Generate Project Tree** (optional) - See what's in your project
2. **Scan Project** - Select files to document
3. **Check Mode** (optional) - Preview what will be generated
4. **Generate Documentation** - Create the markdown files

## Step-by-Step Guide

### Step 1: Navigate to Your Project

```bash
cd /path/to/your/project
```

doc-gen works on whatever directory you run it from.

### Step 2: Launch doc-gen

```bash
doc-gen
```

You'll see the main menu:

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

### Step 3: Generate Project Tree (Optional)

Select option 1 to see your project structure. This helps you understand what doc-gen sees before scanning.

The tree respects your ignore patterns, so you won't see `.git/`, `__pycache__/`, etc.

### Step 4: Scan Project

Select option 2 to scan your project and choose which files to document.

You'll see files one at a time:

```
File 1 of 42: src/main.py
[A]ccept  [S]kip  [Q]uit  [T]oggle auto-accept  [?] = Help

Choice:
```

- Press `A` to include the file
- Press `S` to skip it
- Press `T` to auto-accept all remaining files
- Press `Q` to quit and save what you've selected so far

When done, your selections are saved to `.doc-gen/manifest.yml`.

### Step 5: Check Mode (Optional but Recommended)

Select option 3 to see what you've selected. This shows:

- All selected files
- File sizes
- Syntax highlighting that will be used
- Paginated output so you can review everything

This is your last chance to verify before generating docs.

### Step 6: Generate Documentation

Select option 4 to create the markdown files.

doc-gen will:
- Create `.doc-gen/docs/` directory
- Mirror your project structure
- Generate syntax-highlighted markdown for each file
- Show progress as it works

Output files appear in `.doc-gen/docs/` with the same directory structure as your source files.

## Advanced Workflows

### Updating Documentation

If your source files change, just run the workflow again:

```bash
doc-gen
# Choose option 2 (Scan Project)
# Select new/changed files
# Choose option 4 (Generate Documentation)
```

Your previous manifest is automatically backed up with a timestamp before being replaced.

### Checking Configuration

From the main menu:

```
5. Settings
   1. View Current Configuration
   2. Edit Configuration Path
   3. Manage Ignore Patterns
```

Use these to verify your setup or make changes.

### Starting Fresh

To completely reset:

```bash
rm -rf .doc-gen/
doc-gen
```

This removes all doc-gen state (manifest, config, generated docs) and starts clean.

## Tips

- **Generate tree first** - Helps you see what will be scanned
- **Use Check Mode** - Catch mistakes before generating
- **Auto-accept carefully** - Only use `[T]oggle auto-accept` when you're sure
- **Review manifest** - `.doc-gen/manifest.yml` is human-readable YAML
- **Backup is automatic** - Old manifests go to `.doc-gen/backups/`

## Next Steps

- Learn about [Configuration](configuration.md) to customize behavior
- See [Menu Reference](menu-reference.md) for details on each menu option
- Check [Output Format](output-format.md) to understand generated files

```
