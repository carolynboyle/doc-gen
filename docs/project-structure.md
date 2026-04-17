doc-gen/
├── doc_gen/                      # Main package
│   ├── __init__.py              # Package init, version
│   ├── __main__.py              # Entry point (python -m doc_gen)
│   │
│   ├── core/                    # Core functionality
│   │   ├── __init__.py
│   │   ├── builder.py           # DocumentationBuilder
│   │   ├── scanner.py           # ProjectScanner class
|   |   |__ gitignore.py         # Parse gitignore class
│   │   ├── generator.py         # MarkdownGenerator
│   │   ├── config.py            # Config loading/validation
│   │   └── logger_setup.py      # Logger configuration
│   │
│   ├── ui/                      # User interface
│   │   ├── __init__.py
│   │   ├── menu.py              # MenuSystem
│   │   └── cli.py               # ArgumentParser, CLI handlers
│   │
│   ├── plugins/                 # Plugin system
│   │   ├── __init__.py          # Plugin loader/registry
│   │   ├── base.py              # Base plugin classes
│   │   │
│   │   ├── syntax/              # Syntax detection plugins
│   │   │   ├── __init__.py
│   │   │   ├── base.py          # BaseSyntaxDetector
│   │   │   └── default.py       # DefaultSyntaxDetector
│   │   │
│   │   ├── formatters/          # Output format plugins
│   │   │   ├── __init__.py
│   │   │   ├── base.py          # BaseFormatter
│   │   │   └── markdown.py      # MarkdownFormatter (default)
│   │   │
│   │   └── processors/          # File processors plugins
│   │       ├── __init__.py
│   │       ├── base.py          # BaseFileProcessor
│   │       └── default.py       # DefaultFileProcessor
│   │
│   └── utils/                   # Utility functions
│       ├── __init__.py
│       └── helpers.py           # Common utilities
│
├── plugins/                     # User-installable plugins directory
│   ├── README.md               # How to create plugins
│   └── examples/               # Example plugins
│       ├── syntax_detector_example.py
│       ├── formatter_html.py
│       └── processor_image.py
│
├── doc-gen                      # Executable wrapper (no .py extension)
├── doc-config.yml.template      # Template configuration
├── README.md                    # Main documentation
├── PLUGIN_GUIDE.md             # Plugin development guide
├── LICENSE
├── setup.py                     # Package installation
├── .gitignore
│
├── examples/                    # Example projects to test against
│   ├── sample-python/
│   │   ├── scripts/
│   │   ├── configs/
│   │   └── .gitignore
│   └── sample-shell/
│       ├── bin/
│       └── .gitignore
│
└── tests/                       # Unit tests
    ├── __init__.py
    ├── test_scanner.py
    ├── test_generator.py
    ├── test_plugins.py
    └── fixtures/                # Test data
        └── sample_files/

