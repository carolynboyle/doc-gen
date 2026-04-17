# installation.md

**Path:** docs/installation.md
**Syntax:** markdown
**Generated:** 2026-03-26 19:01:15

```markdown
# Installation

## Requirements

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/carolynboyle/doc-gen.git
cd doc-gen
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows
```

### 3. Install Package

```bash
pip install -e .
```

The `-e` flag installs in editable mode, which is useful if you want to modify the code.

### 4. Verify Installation

```bash
doc-gen --version
```

You should see the version number printed.

## Alternative: Install from PyPI

Once published to PyPI, you'll be able to install with:

```bash
pip install doc-gen
```

(Not yet available - currently install from source only)

## Troubleshooting

### Virtual Environment Not Activated

If you see an error about virtual environment not being activated:

```bash
source .venv/bin/activate  # Run this first
doc-gen                     # Then run doc-gen
```

### Permission Issues

If you get permission errors during installation:

```bash
# Try installing with --user flag
pip install --user -e .
```

### Template File Not Found

If you get errors about missing template files after installation:

```bash
pip uninstall doc-gen
pip install -e .
```

For more troubleshooting help, see the [Troubleshooting Guide](troubleshooting.md).

## Next Steps

Once installed, head over to [Workflows](workflows.md) to learn how to use doc-gen.

```
