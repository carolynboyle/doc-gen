# test_prompt.py

**Path:** tests/test_prompt.py
**Syntax:** python
**Generated:** 2026-03-26 19:01:15

```python
#!/usr/bin/env python3
"""Quick test of the prompt_file_selection function"""

from pathlib import Path
from doc_gen.utils.prompts import prompt_file_selection

# Test with some fake file paths
test_files = [
    Path("/home/user/projects/doc-gen/doc_gen/core/scanner.py"),
    Path("/home/user/projects/doc-gen/README.md"),
    Path("/home/user/projects/doc-gen/doc_gen/utils/prompts.py"),
]

project_root = Path("/home/user/projects/doc-gen")

print("Testing file selection prompts...")
print("(Try: Y, n, Enter, yes, no, invalid input)\n")

results = []
for filepath in test_files:
    selected = prompt_file_selection(filepath, relative_to=project_root)
    results.append((filepath.name, selected))
    print(f"  → {'INCLUDED' if selected else 'SKIPPED'}\n")

print("\n=== Summary ===")
for name, selected in results:
    status = "✓" if selected else "✗"
    print(f"{status} {name}")
```
