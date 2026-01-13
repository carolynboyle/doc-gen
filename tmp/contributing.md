# Contributing

Thank you for your interest in contributing to doc-gen! This guide will help you get started.

## Project Status

doc-gen is currently a learning project built by someone new to Python (but with 40 years of programming experience). It's being shared for class feedback and is in active development.

**What this means for contributors:**
- All skill levels welcome
- Learning together is encouraged
- Questions are valuable feedback
- Suggestions help improve the project

## Ways to Contribute

### 1. Use It and Report Issues

The most valuable contribution is using doc-gen and reporting:
- Bugs you encounter
- Confusing behavior
- Missing features
- Documentation gaps

**How to report:**
1. Check [existing issues](https://github.com/carolynboyle/doc-gen/issues) first
2. Create new issue with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version)

### 2. Improve Documentation

Documentation improvements are always welcome:
- Fix typos
- Clarify confusing sections
- Add examples
- Improve organization

**Easy starting point:** If something confused you, it probably confuses others too. Document what you learned!

### 3. Write Tests

Test coverage can always be better:
- Unit tests for core classes
- Integration tests for workflows
- Edge case testing
- Performance benchmarks

See `tests/` directory for existing tests.

### 4. Add Features

Before starting on a feature:
1. Check [Roadmap](roadmap.md) to see if it's planned
2. Open an issue to discuss approach
3. Get feedback before writing code

**Why:** Prevents wasted effort on features that won't be merged.

### 5. Create Plugins

The plugin system needs:
- Example plugins
- Documentation
- Testing
- Real-world use cases

See `plugins/examples/` for inspiration.

## Development Setup

### 1. Fork and Clone

```bash
# Fork on GitHub, then:
git clone https://github.com/YOUR-USERNAME/doc-gen.git
cd doc-gen
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows
```

### 3. Install in Editable Mode

```bash
pip install -e .
```

This lets you test your changes immediately.

### 4. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-number
```

### 5. Make Your Changes

Edit code, add tests, update docs as needed.

### 6. Test Your Changes

```bash
# Run existing tests
python -m pytest tests/

# Test manually with doc-gen
cd /path/to/test/project
doc-gen
```

### 7. Commit and Push

```bash
git add .
git commit -m "Clear description of changes"
git push origin feature/your-feature-name
```

### 8. Create Pull Request

On GitHub, create a pull request from your branch to `main`.

**In your PR description:**
- What problem does this solve?
- How did you test it?
- Any breaking changes?
- Screenshots if UI changes

## Code Style

### General Guidelines

- **Follow existing patterns** - Consistency matters
- **Use type hints** - Helps with IDE support and clarity
- **Add docstrings** - Especially for public methods
- **Keep functions focused** - One responsibility per function
- **Avoid deep nesting** - Extract complex logic

### Python Style

Following PEP 8 with some flexibility:
- 4 spaces for indentation
- 88 character line length (Black default)
- Descriptive variable names
- Comments for non-obvious code

### Example

```python
def process_file(file_path: Path, config: dict) -> dict:
    """Process a single file and return result.
    
    Args:
        file_path: Path to file to process
        config: Configuration dictionary
        
    Returns:
        Dictionary with 'success', 'message', 'data' keys
    """
    try:
        content = file_path.read_text()
        # Processing logic here
        return {
            'success': True,
            'message': 'File processed',
            'data': content
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Error: {e}',
            'data': None
        }
```

## Commit Message Guidelines

**Format:**
```
<type>: <short description>

<optional longer description>
<optional reference to issue>
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation only
- `style:` Code style (formatting, no logic change)
- `refactor:` Code restructuring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

**Examples:**
```
feat: Add single-page documentation mode

Implements consolidated markdown output with hyperlinked TOC.
Closes #42

---

fix: Handle empty manifest gracefully

Previously crashed when manifest.yml was empty.
Now shows helpful error message.
Fixes #38

---

docs: Clarify configuration syntax in README

Users were confused about YAML indentation.
Added examples and common mistakes section.
```

## Testing Guidelines

### What to Test

- **Happy path** - Normal usage
- **Edge cases** - Empty inputs, large files, special characters
- **Error cases** - Invalid inputs, missing files, permission errors
- **Integration** - Full workflow end-to-end

### Writing Tests

Use pytest:

```python
def test_scan_respects_gitignore(tmp_path):
    """Scanner should exclude files matching .gitignore patterns."""
    # Setup
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    (project_dir / ".gitignore").write_text("*.log\n")
    (project_dir / "test.log").write_text("log content")
    (project_dir / "test.py").write_text("python content")
    
    # Execute
    scanner = ProjectScanner(project_dir)
    files = scanner.scan_files()
    
    # Assert
    assert "test.py" in [f.name for f in files]
    assert "test.log" not in [f.name for f in files]
```

## Review Process

Pull requests are reviewed for:
1. **Functionality** - Does it work as intended?
2. **Tests** - Are there tests? Do they pass?
3. **Documentation** - Is it documented?
4. **Style** - Does it follow conventions?
5. **Breaking changes** - Are they necessary and documented?

**Timeline:** Reviews happen when time permits. This is a side project, so please be patient.

## Questions?

Not sure about something? Ask!

- Open an issue for discussion
- Comment on existing issues
- Reach out via GitHub

No question is too basic. If you're confused, others probably are too.

## Code of Conduct

### Be Respectful

- Welcome all skill levels
- Assume good intentions
- Provide constructive feedback
- Help others learn

### Be Professional

- Focus on the code, not the person
- Accept feedback gracefully
- Give credit where due
- Keep discussions on topic

### Be Patient

- This is a learning project
- Reviews take time
- Not all PRs will be merged
- Feedback helps everyone improve

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md (if we create one)
- Credited in release notes
- Thanked profusely

## License

By contributing, you agree that your contributions will be licensed under the same MIT License that covers the project.

## Thank You!

Every contribution helps make doc-gen better. Whether it's:
- A bug report
- A typo fix
- A new feature
- Just using the tool and sharing feedback

**Thank you for being part of doc-gen!**

## Next Steps

- Check [Roadmap](roadmap.md) for ideas
- Browse [open issues](https://github.com/carolynboyle/doc-gen/issues)
- Read [Design Philosophy](design-philosophy.md) to understand the vision
- Start small - documentation fixes are great first contributions!
