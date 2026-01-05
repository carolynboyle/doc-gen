# test_manifest.py

**Path:** tests/test_manifest.py
**Syntax:** python
**Generated:** 2026-01-03 17:24:45

```python
#!/usr/bin/env python3
"""Quick test of manifest read/write functions"""

from pathlib import Path
from doc_gen.core.manifest import write_manifest, read_manifest

# Simulate some selected files
project_root = Path.cwd()
selected_files = [
    project_root / "doc_gen/core/scanner.py",
    project_root / "doc_gen/core/config.py",
    project_root / "doc_gen/utils/prompts.py",
    project_root / "README.md",
]

print("=== Testing Manifest Writer ===\n")

# Write manifest
print("Writing manifest with 4 test files...")
result = write_manifest(selected_files, project_root, "test-manifest.yml")

if result['success']:
    print(f"✓ {result['message']}")
    print(f"  Files written: {result['count']}\n")
else:
    print(f"✗ {result['message']}\n")
    exit(1)

# Show the generated file
print("=== Generated Manifest Content ===")
with open("test-manifest.yml") as f:
    print(f.read())

# Read it back
print("=== Testing Manifest Reader ===\n")
result = read_manifest("test-manifest.yml")

if result['success']:
    print(f"✓ {result['message']}")
    print(f"\nDocuments read:")
    for doc in result['documents']:
        print(f"  - {doc}")
else:
    print(f"✗ {result['message']}")

print("\n✓ Test complete! Check test-manifest.yml to see the output.")
```
