"""
Menu action handlers for doc-gen.
Contains all the actual functionality behind menu options.
"""
from pathlib import Path
import os
import pydoc
import subprocess
import yaml
from doc_gen.core.config import ensure_doc_gen_structure, OUTPUT_DIR
from doc_gen.core.config import (
    initialize_config as init_config, 
    load_config,
    DEFAULT_MANIFEST_PATH,
    OUTPUT_DIR,
    get_ignore_patterns,
    reset_ignore_patterns as reset_patterns,
    add_ignore_pattern as add_pattern,
    remove_ignore_pattern as remove_pattern,
    IGNORE_PATTERNS_FILE,
    HARDCODED_IGNORES
)
from doc_gen.core.builder import run_interactive_mode, run_generate_mode, run_check_mode
# from doc_gen.core.manifest import read_manifest
# from doc_gen.core.scanner import ProjectScanner
# from doc_gen.utils.prompts import prompt_file_selection
# from doc_gen.utils.tree import generate_project_tree, save_project_tree



class MenuActions:
    """Handlers for menu actions."""
    
    def __init__(self, menu_system):
        """
        Initialize menu actions.
        
        Args:
            menu_system: Reference to parent MenuSystem for accessing config
        """
        self.menu = menu_system
        
        # Ignore patterns submenu dispatch
        self.ignore_patterns_actions = {
            '1': self.view_ignore_patterns,
            '2': self.reset_ignore_patterns,
            '3': self.add_ignore_pattern,
            '4': self.remove_ignore_pattern,
            '5': self.edit_ignore_patterns_file,
            '6': self.back_from_ignore_patterns
        }
    
    # Main Menu Actions
    
    def scan_project(self):
        """Scan project and select files to document (build manifest)."""
        self.menu.clear_screen()
        self.menu.display_header("Scan Project - Select Files to Document")
        
        print("\nFiles matching ignore patterns will be skipped")
        print("(.venv/, .git/, __pycache__/, etc.)")
        print(".doc-gen/ is always excluded (tool never documents itself)")
        print("=" * 60)
        
        # Get project path from user (or use current directory)
        project_path = input("\nProject directory to scan (Enter for current directory): ").strip()
        if not project_path:
            project_path = None  # Will default to current directory
        
        # Run scan and selection (respects ignore patterns automatically)
        result = run_interactive_mode(
            project_root=project_path,
            config_path=self.menu.current_config
        )
        
        # Clear screen before showing result (prevents scroll spam from rapid Enter)
        self.menu.clear_screen()
        
        # Display result
        print(f"\n{result['message']}")
        
        if not result['success']:
            print("(Scan did not complete successfully)")
        
        input("\nPress Enter to continue...")
    
    def generate_docs(self):
        """Generate documentation from existing manifest."""
        self.menu.clear_screen()
        self.menu.display_header("Generate Documentation from Selected Files")
        
        # Get manifest path from user (or use default)
        manifest_path = input(f"\nName for selected files list (Enter for default): ").strip()
        if not manifest_path:
            manifest_path = str(DEFAULT_MANIFEST_PATH)
        
        # Run generate mode
        result = run_generate_mode(
            manifest_path=manifest_path,
            config_path=self.menu.current_config
        )
        
        # Display result
        print(f"\n{result['message']}")
        
        if not result['success']:
            print("(Generation did not complete successfully)")
            print("\nNo files selected yet:")
            print("  1. Use option 2: 'Scan Project' to select files")
            print("  2. Choose which files to document")
            print("  3. Then return here to generate documentation")
        
        input("\nPress Enter to continue...")
    
    def check_mode(self):
        """Dry-run mode to check what would be generated."""
        self.menu.clear_screen()
        self.menu.display_header("Check Mode - Dry Run")
        
        # Get manifest path from user (or use default)
        manifest_path = input(f"\nManifest file (Enter for '{DEFAULT_MANIFEST_PATH}'): ").strip()
        if not manifest_path:
            manifest_path = str(DEFAULT_MANIFEST_PATH)
        
        print("\nRunning check mode...")
        
        # Run check mode
        result = run_check_mode(
            manifest_path=manifest_path,
            config_path=self.menu.current_config
        )
        
        if result['success']:
            # Use pager to display report
            pydoc.pager(result['report'])
            
            # Offer to save to file
            save = input("\nSave report to file? (y/N): ").strip().lower()
            if save == 'y':
                filename = input("Filename (Enter for '.doc-gen/check-report.txt'): ").strip()
                if not filename:
                    filename = ".doc-gen/check-report.txt"
                
                try:
                    Path(filename).write_text(result['report'], encoding='utf-8')
                    print(f"Report saved to {Path(filename).absolute()}")
                except Exception as e:
                    print(f"Error saving file: {e}")
            
            input("\nPress Enter to continue...")
        else:
            # Error - just print message
            print(f"\n{result['message']}")
            input("\nPress Enter to continue...")
    
    def initialize_config(self):
        """Create configuration template from doc-config.yml.template."""
        self.menu.clear_screen()
        self.menu.display_header("Initialize Configuration")
        
        # Call the real function from config module
        result = init_config()
        
        # Display the result
        print(f"\n{result['message']}")
        
        if not result['success']:
            print("(Config initialization failed)")
        
        input("\nPress Enter to continue...")
    
   

    def get_project_tree(self):
        """Generate and display project filesystem tree."""
        self.menu.clear_screen()
        self.menu.display_header("Project Filesystem Tree")

        result = ensure_doc_gen_structure()
        if not result["success"]:
            print(f"\nError: {result['message']}")
            input("\nPress Enter to continue...")
            return

        output_name = input(
            "\nOutput filename (Enter for 'project-tree.txt'): "
        ).strip() or "project-tree.txt"

        output_path = Path(OUTPUT_DIR) / output_name

        try:
            proc = subprocess.run(
                ["tree", "-a", "-F"],
                check=False,
                capture_output=True,
                text=True,
            )
        except FileNotFoundError:
            print("\nError: 'tree' command not found. Please install it.")
            input("\nPress Enter to continue...")
            return

        # Page the output (long!)
        pydoc.pager(proc.stdout)

        # Save to file
        output_path.write_text(proc.stdout, encoding="utf-8")

        print(f"\nTree saved to: {output_path.resolve()}")
        print(f"Lines written: {len(proc.stdout.splitlines())}")

        input("\nPress Enter to continue...")

    def view_config(self):
        """Display current configuration with pagination."""
        self.menu.clear_screen()

        result = load_config(self.menu.current_config)

        if result['success']:
            config_path = Path(self.menu.current_config).resolve()

            header = (
                "=" * 60 + "\n"
                f"Configuration from: {config_path}\n"
                + "=" * 60 + "\n\n"
            )

            config_text = header + yaml.dump(
            result['config'],
            default_flow_style=False,
            sort_keys=False
            )

            pydoc.pager(config_text)
        else:
            print(f"\nError loading config: {result['message']}")
            input("\nPress Enter to continue...")

        input("\nPress Enter to continue...")
    
    def edit_config_path(self):
        """Change configuration file path."""
        self.menu.clear_screen()
        self.menu.display_header("Edit Configuration Path")
        
        # Show full resolved path
        current_full = Path(self.menu.current_config).resolve()
        print(f"Current: {current_full}")
        
        new_path = input("Enter new path (or Enter to cancel): ").strip()
        if new_path:
            self.menu.current_config = new_path
            print(f"Configuration path updated to: {Path(new_path).resolve()}")
        
        input("\nPress Enter to continue...")
    
    def view_plugins(self):
        """Show plugin status."""
        self.menu.clear_screen()
        self.menu.display_header("Plugin Status")
        print("This will show loaded plugins and their status")
        input("\nPress Enter to continue...")
    
    # Ignore Patterns Management
    
    def manage_ignore_patterns(self):
        """Main submenu for managing ignore patterns."""
        while True:
            self.menu.clear_screen()
            self.menu.display_header("Manage Ignore Patterns")
            print(f"File: {IGNORE_PATTERNS_FILE.resolve()}\n")
            print("1. View Current Patterns")
            print("2. Reset to Defaults (from .gitignore)")
            print("3. Add New Pattern")
            print("4. Remove Pattern")
            print("5. Edit File Directly")
            print("6. Back to Settings")
            print()
            
            choice = self.menu.get_choice(self.ignore_patterns_actions.keys(), self.display_ignore_patterns_menu)
            
            # Execute selected action
            action = self.ignore_patterns_actions[choice]
            result = action()
            
            # Break back to settings if requested
            if result == 'back':
                break
    
    def display_ignore_patterns_menu(self):
        """Display ignore patterns menu (for error handling)."""
        self.menu.display_header("Manage Ignore Patterns")
        print(f"File: {IGNORE_PATTERNS_FILE.resolve()}\n")
        print("1. View Current Patterns")
        print("2. Reset to Defaults (from .gitignore)")
        print("3. Add New Pattern")
        print("4. Remove Pattern")
        print("5. Edit File Directly")
        print("6. Back to Settings")
        print()
    
    def view_ignore_patterns(self):
        """Display current ignore patterns with line numbers."""
        self.menu.clear_screen()
        self.menu.display_header("Current Ignore Patterns")
        
        result = get_ignore_patterns()
        
        if result['success']:
            # Format with line numbers
            patterns_text = f"Ignore patterns from: {IGNORE_PATTERNS_FILE.resolve()}\n\n"
            
            for i, line in enumerate(result['patterns'], 1):
                # Highlight hardcoded patterns
                if any(hc in line for hc in HARDCODED_IGNORES) and not line.startswith('#'):
                    patterns_text += f"{i:4d}  {line} [HARDCODED - cannot remove]\n"
                else:
                    patterns_text += f"{i:4d}  {line}\n"
            
            # Use pager
            pydoc.pager(patterns_text)
        else:
            print(f"\nError: {result['message']}")
        
        input("\nPress Enter to continue...")
    
    def reset_ignore_patterns(self):
        """Reset ignore patterns to defaults."""
        self.menu.clear_screen()
        self.menu.display_header("Reset Ignore Patterns")
        
        print("\nThis will reset ignore patterns to defaults.")
        print("Current file will be backed up to .doc-gen/backups/")
        print()
        
        confirm = input("Continue? (y/N): ").strip().lower()
        
        if confirm == 'y':
            result = reset_patterns()
            print(f"\n{result['message']}")
        else:
            print("\nReset cancelled")
        
        input("\nPress Enter to continue...")
    
    def add_ignore_pattern(self):
        """Add a new ignore pattern."""
        self.menu.clear_screen()
        self.menu.display_header("Add Ignore Pattern")
        
        print("\nEnter pattern to ignore (e.g., '*.log' or '.venv/')")
        print("Use trailing '/' for directories")
        print()
        
        pattern = input("Pattern (or Enter to cancel): ").strip()
        
        if pattern:
            result = add_pattern(pattern)
            print(f"\n{result['message']}")
        else:
            print("\nCancelled")
        
        input("\nPress Enter to continue...")
    
    def remove_ignore_pattern(self):
        """Remove an ignore pattern by line number."""
        self.menu.clear_screen()
        self.menu.display_header("Remove Ignore Pattern")
        
        # Show current patterns
        result = get_ignore_patterns()
        
        if not result['success']:
            print(f"\nError: {result['message']}")
            input("\nPress Enter to continue...")
            return
        
        print("\nCurrent patterns:\n")
        for i, line in enumerate(result['patterns'], 1):
            if any(hc in line for hc in HARDCODED_IGNORES) and not line.startswith('#'):
                print(f"{i:4d}  {line} [HARDCODED]")
            else:
                print(f"{i:4d}  {line}")
        
        print("\nEnter line number to remove (or Enter to cancel)")
        print("Note: Hardcoded patterns cannot be removed")
        print()
        
        choice = input("Line number: ").strip()
        
        if choice:
            try:
                line_num = int(choice)
                result = remove_pattern(line_num)
                print(f"\n{result['message']}")
            except ValueError:
                print(f"\nError: Invalid line number '{choice}'")
        else:
            print("\nCancelled")
        
        input("\nPress Enter to continue...")
    
    def edit_ignore_patterns_file(self):
        """Open ignore patterns file in user's editor."""
        self.menu.clear_screen()
        self.menu.display_header("Edit Ignore Patterns File")
        
        # Get editor from environment
        editor = os.environ.get('EDITOR', 'nano')
        
        print(f"\nOpening {IGNORE_PATTERNS_FILE.resolve()}")
        print(f"Editor: {editor}")
        print()
        print("Note: Hardcoded patterns (.doc-gen/, .git/, __pycache__/)")
        print("      are enforced regardless of file contents")
        print()
        
        input("Press Enter to open editor...")
        
        try:
            subprocess.run([editor, str(IGNORE_PATTERNS_FILE)])
            print("\nFile edited successfully")
        except Exception as e:
            print(f"\nError opening editor: {e}")
            print(f"You can manually edit: {IGNORE_PATTERNS_FILE.resolve()}")
        
        input("\nPress Enter to continue...")
    
    def back_from_ignore_patterns(self):
        """Return to settings menu."""
        return 'back'