# Troubleshooting

Common issues and their solutions.

## Installation Issues

### Template File Not Found

**Error:**
```
Template file not found at /path/to/doc-config.yml.template
(Config initialization failed)
```

**Cause:** The package template file is missing or wasn't included in installation.

**Solution:**
```bash
# Reinstall the package
pip uninstall doc-gen
pip install -e .

# Or if installed from GitHub/PyPI:
pip install --force-reinstall doc-gen
```

**Prevention:** If developing doc-gen, ensure `MANIFEST.in` exists and includes the template file.

### Virtual Environment Not Activated

**Error:**
```
⚠️  ERROR: Virtual environment not activated!
```

**Cause:** doc-gen requires running inside a virtual environment for dependency isolation.

**Solution:**
```bash
# Linux/Mac:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate

# Then run doc-gen again
doc-gen
```

### Cannot Create .doc-gen/ Directory

**Error:**
```
❌ ERROR: Cannot create .doc-gen/ directory
Permission denied: Cannot create /path/to/project/.doc-gen
```

**Cause:** Insufficient permissions in the current directory.

**Solutions:**
1. Check directory permissions: `ls -la`
2. Ensure you own the directory: `sudo chown -R $USER:$USER /path/to/project`
3. Try running from a directory you have write access to
4. Check if filesystem is read-only

## Runtime Issues

### Clipboard Problems (KDE)

**Symptom:** Paste operations fail or paste incorrect content in terminal.

**Workarounds:**
1. Use CopyQ clipboard manager (more reliable than Klipper)
2. Type small snippets manually
3. Use file-based transfer (save to file, copy file)
4. Copy in smaller chunks

**Note:** This is not a doc-gen bug - it's a known KDE/terminal clipboard issue.

### Scanner Finds Too Many Files

**Symptom:** Scanner shows thousands of files including `.git/`, `node_modules/`, etc.

**Cause:** Ignore patterns file not properly configured.

**Solution:**
1. Go to Settings → Manage Ignore Patterns
2. Check that patterns are loaded
3. Reset to defaults if needed (backs up current file)
4. Verify `.doc-gen/ignore-patterns.txt` exists

**Expected behavior:** `.doc-gen/`, `.git/`, and `__pycache__/` are ALWAYS ignored (hardcoded).

### Generated Markdown Has Wrong Syntax Highlighting

**Symptom:** Code blocks show as plain text or wrong language.

**Cause:** File extension not mapped in config, or config not loaded.

**Solution:**
1. Check current config: Settings → View Current Configuration
2. Edit `.doc-gen/config.yml`
3. Add mapping under `syntax_map:`:
   ```yaml
   syntax_map:
     .myext: mylanguage
   ```
4. Common languages: python, bash, javascript, yaml, json, markdown

### Manifest Not Found

**Error:**
```
✗ Manifest not found: .doc-gen/manifest.yml
```

**Cause:** Haven't run scan/selection yet.

**Solution:**
1. Go to Option 2: "Scan Project - Select files to document"
2. Select which files to include
3. Manifest will be created at `.doc-gen/manifest.yml`
4. Then run Option 4: "Generate Documentation"

**Workflow:** Always scan → select → generate

### Binary Files in Scan Results

**Symptom:** Scanner reports many binary files detected.

**This is normal!** Binary files (images, PDFs, compiled code, `.git/` objects) are automatically detected and skipped. They're shown in stats for transparency but don't affect documentation generation.

To hide from tree: Binary files are already excluded from manifest. Project tree generation respects this.

## Configuration Issues

### Config Changes Not Taking Effect

**Cause:** Config is cached or using wrong config file.

**Solution:**
1. Check which config is loaded: Shows at top of main menu
2. Change config path: Settings → Edit Configuration Path
3. Restart doc-gen
4. Verify config file location: Should be `.doc-gen/config.yml`

### Ignore Patterns Not Working

**Symptoms:**
- Files that should be ignored are appearing
- Pattern syntax seems correct

**Debugging:**
1. Settings → Manage Ignore Patterns → View Current Patterns
2. Check line numbers for typos
3. Remember patterns are NOT regular expressions:
   - Use `*.log` not `.*\.log`
   - Use `.venv/` for directories (trailing slash)
   - Use `*.pyc` for file globs
4. Hardcoded patterns (`.doc-gen/`, `.git/`, `__pycache__/`) cannot be removed

**Common mistakes:**
```bash
# WRONG:
.*.pyc          # Don't use regex syntax
.venv           # Missing trailing slash for directory

# RIGHT:
*.pyc           # Simple glob
.venv/          # Directory pattern
```

## Performance Issues

### Scanning Very Large Projects

**Symptom:** Scan takes minutes, thousands of files found.

**Solutions:**
1. Add common large directories to ignore patterns:
   - `node_modules/`
   - `vendor/`
   - `target/`
   - `build/`
   - `dist/`
2. Ensure `.gitignore` is comprehensive (patterns are copied from it)
3. Use project tree generation to verify what's included before scanning

### Generation Taking Too Long

**Symptom:** Documentation generation hangs or takes minutes.

**Causes:**
- Very large files in manifest
- Many files selected
- Slow disk I/O

**Solutions:**
1. Run Check Mode first (Option 3) to see what will be generated
2. Remove very large files from manifest if not needed
3. Generate in smaller batches

## Menu & Navigation Issues

### Rapid Keypresses Cause Issues

**Symptom:** Pressing Enter repeatedly causes skipped prompts or unexpected behavior.

**Status:** This should be fixed in current version. If you still encounter it, please report as a bug.

### Can't Exit Menu

**Solution:**
- Main menu: Select option 6 (Exit)
- Submenus: Look for "Return to..." option
- File selection: Press `Q` to quit
- Emergency: Ctrl+C works (state is saved)

## Getting Help

### Still Stuck?

1. **Check TODO.md** for known issues and future enhancements
2. **Check GitHub Issues**: https://github.com/carolynboyle/doc-gen/issues
3. **File a bug report** with:
   - Full error message
   - Steps to reproduce
   - Your OS and Python version
   - Output of `pip show doc-gen`

### Debug Information

For debugging, examine these files:
- `.doc-gen/manifest.yml` - List of selected files
- `.doc-gen/ignore-patterns.txt` - Active ignore patterns
- `.doc-gen/config.yml` - Configuration settings
- `.doc-gen/backups/` - Backup copies of manifests

All doc-gen state is in `.doc-gen/` - safe to delete and start fresh if needed.

### Fresh Start

If all else fails, start completely fresh:

```bash
# Back up anything important from .doc-gen/ first!
rm -rf .doc-gen/
doc-gen
```

This removes all doc-gen state and starts clean.

## Reporting Bugs

When reporting issues on GitHub, please include:

1. **Error message** (complete text)
2. **Steps to reproduce** (exactly what you did)
3. **Expected behavior** (what should have happened)
4. **Actual behavior** (what did happen)
5. **Environment:**
   - OS (Linux/Mac/Windows)
   - Python version (`python --version`)
   - doc-gen version (`pip show doc-gen`)
6. **Relevant files** (config.yml, manifest.yml if applicable)

## Next Steps

- Review [Workflows](workflows.md) for correct usage
- Check [Configuration](configuration.md) for settings
- See [Design Philosophy](design-philosophy.md) to understand expected behavior
