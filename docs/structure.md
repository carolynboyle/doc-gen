**From refactor discussion 2026JAN16:**

doc-gen/
├── doc_gen/
│   ├── __init__.py
│   ├── core/
│   │   ├─✔️─ __init__.py 
│   │   ├─✔️─ config.py          # REPLACE with config_refactored.py
│   │   ├─✔️─ engine.py           # NEW - create from engine.py
│   │   ├─✔️─ builder.py          # EXISTING - no changes needed
│   │   ├── scanner.py          # EXISTING - update imports to use DocGenConfig
│   │   ├─✔️─ generator.py        # EXISTING - update imports to use DocGenConfig
│   │   └── manifest.py         # EXISTING - update imports to use DocGenConfig
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── menu.py             # MODIFY - change menu text
│   │   ├── menu_actions.py     # REFACTOR - strip to pure UI
│   │   └── cli.py              # NEW - create CLI interface
│   ├── utils/
│   │   ├── __init__.py
│   │   └── prompts.py          # EXISTING - no changes
│   ├── plugins/
│   │   └── __init__.py
│   └── data/                   # NEW DIRECTORY
│       └── defaults.yml        # NEW - from defaults.yml
├── doc-config.yml.template     # EXISTING - consider updating with new options
├── pyproject.toml              # MODIFY - add data files
├── README.md
└── TODO.md