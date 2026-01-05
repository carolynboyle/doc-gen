"""
Menu action handlers for doc-gen.
Contains all the actual functionality behind menu options.
"""

from pathlib import Path
import os
import pydoc
from doc_gen.core.config import (
    initialize_config as init_config, 
    load_config,
    DEFAULT_MANIFEST_PATH,
    OUTPUT_DIR
)
from doc_gen.core.builder import run_interactive_mode, run_generate_mode, run_check_mode
from doc_gen.core.scanner import ProjectScanner
from doc_gen.utils.prompts import prompt_file_selection
from doc_gen.utils.tree import generate_project_tree, save_project_tree
import yaml


class MenuActions:
    """Handlers for menu actions."""
    
    def __init__(self, menu_system):
        """
        Initialize menu actions.
        
        Args:
            menu_system: Reference to parent MenuSystem for accessing config
        """
        self.menu = menu_system
    
    # Main Menu Actions
    
    def interactive_mode(self):
        """Scan project and select files to document (build manifest)."""
        self.menu.clear_screen()
        self.menu.display_header("Scan Project - Select Files to Document")
        
        print("\n" + "=" * 50)
        print("NOTE: Files matching .gitignore patterns will be skipped")
        print("This includes .venv/, .git/, __pycache__/, etc.")
        print(".doc-gen/ is ALWAYS excluded (tool never documents itself)")
        print("To include gitignored files in project tree, use")
        print("'Generate Project Tree' option after selecting files.")
        print("=" * 50)
        
        # Get project path from user (or use current directory)
        project_path = input("\nProject directory to scan (Enter for current directory): ").strip()
        if not project_path:
            project_path = None  # Will default to current directory
        
        # Run interactive mode
        result = run_interactive_mode(
            project_root=project_path,
            config_path=self.menu.current_config
        )
        
        # Display result
        print(f"\n{result['message']}")
        
        if not result['success']:
            print("(Interactive mode did not complete successfully)")
        
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
        """Dry-run mode to show what will be created."""
        self.menu.clear_screen()
        self.menu.display_header("Check Mode - Show What Will Be Created")
        
        # Get manifest path from user (or use default)
        manifest_path = input(f"\nName for selected files list (Enter for default): ").strip()
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
                while True:
                    filename = input("Filename (Enter for '.doc-gen/check-report.txt'): ").strip()
                    if not filename:
                        filename = ".doc-gen/check-report.txt"
                    
                    # Expand user path (~ to /home/user)
                    filepath = Path(filename).expanduser().resolve()
                    
                    # Check if it's a directory
                    if filepath.exists() and filepath.is_dir():
                        print(f"\n✗ '{filename}' is a directory, not a file")
                        print(f"Please specify a filename, e.g., '{filepath}/check-report.txt'")
                        retry = input("Try again? (Y/n): ").strip().lower()
                        if retry == 'n':
                            break
                        continue
                    
                    # Try to create parent directory
                    try:
                        filepath.parent.mkdir(parents=True, exist_ok=True)
                    except PermissionError:
                        print(f"\n✗ Permission denied: Cannot create directory {filepath.parent}")
                        retry = input("Try a different path? (y/N): ").strip().lower()
                        if retry != 'y':
                            break
                        continue
                    except Exception as e:
                        print(f"\n✗ Error creating directory: {e}")
                        retry = input("Try a different path? (y/N): ").strip().lower()
                        if retry != 'y':
                            break
                        continue
                    
                    # Try to write the file
                    try:
                        filepath.write_text(result['report'], encoding='utf-8')
                        if filepath.exists():
                            print(f"\n✓ Report saved to {filepath}")
                            break
                        else:
                            print(f"\n✗ Failed to create file")
                            retry = input("Try a different path? (y/N): ").strip().lower()
                            if retry != 'y':
                                break
                    except PermissionError:
                        print(f"\n✗ Permission denied: Cannot write to {filepath}")
                        retry = input("Try a different path? (y/N): ").strip().lower()
                        if retry != 'y':
                            break
                    except Exception as e:
                        print(f"\n✗ Error saving file: {e}")
                        retry = input("Try a different path? (y/N): ").strip().lower()
                        if retry != 'y':
                            break
            
            input("\nPress Enter to continue...")
        else:
            # Error - just print message
            print(f"\n{result['message']}")
            print("\nNo files selected yet:")
            print("  1. Use option 2: 'Scan Project' to select files")
            print("  2. Choose which files to document")
            print("  3. Then return here to run check mode")
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
    
    def generate_tree(self):
        """Generate project tree structure file (standalone utility)."""
        self.menu.clear_screen()
        self.menu.display_header("Generate Project Tree")
        
        project_root = Path.cwd()
        gitignore_path = project_root / '.gitignore'
        
        print("\nThis will generate a project structure visualization.")
        print("By default, .gitignore patterns are respected.")
        print("You can choose to include specific patterns.\n")
        
        # Start with files respecting .gitignore
        scanner = ProjectScanner(
            root_dir=project_root,
            gitignore_path=gitignore_path if gitignore_path.exists() else None,
            exclusions=[]
        )
        files_to_include = scanner.scan_files()
        
        # Always exclude .doc-gen (hardcoded)
        files_to_include = [f for f in files_to_include if '.doc-gen' not in f.parts]
        
        print(f"Found {len(files_to_include)} files (respecting .gitignore)\n")
        
        # Ask about including gitignored patterns
        if gitignore_path.exists():
            include_ignored = input("Include some gitignored patterns? (y/N): ").strip().lower()
            
            if include_ignored == 'y':
                print("\n" + "=" * 50)
                print("Select .gitignore patterns to INCLUDE in tree:")
                print("=" * 50 + "\n")
                
                # Read and parse .gitignore
                gitignore_lines = gitignore_path.read_text().splitlines()
                patterns_to_include = []
                
                for line in gitignore_lines:
                    line = line.strip()
                    
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    
                    # Prompt for this pattern
                    response = input(f"Include files matching '{line}'? (y/N): ").strip().lower()
                    if response == 'y':
                        patterns_to_include.append(line)
                
                # Scan for files matching the included patterns
                if patterns_to_include:
                    print(f"\nScanning for files matching {len(patterns_to_include)} selected patterns...")
                    
                    # Scan without gitignore
                    full_scanner = ProjectScanner(
                        root_dir=project_root,
                        gitignore_path=None,
                        exclusions=[]
                    )
                    all_files = full_scanner.scan_files()
                    
                    # Find files matching selected patterns
                    from fnmatch import fnmatch
                    already_included = set(str(f) for f in files_to_include)
                    
                    for filepath in all_files:
                        # Skip if already included or in .doc-gen
                        if str(filepath) in already_included or '.doc-gen' in filepath.parts:
                            continue
                        
                        # Check if matches any selected pattern
                        for pattern in patterns_to_include:
                            # Handle directory patterns (end with /)
                            if pattern.endswith('/'):
                                dir_pattern = pattern.rstrip('/')
                                if dir_pattern in filepath.parts:
                                    files_to_include.append(filepath)
                                    break
                            else:
                                # File pattern
                                if fnmatch(filepath.name, pattern):
                                    files_to_include.append(filepath)
                                    break
                    
                    print(f"Tree will include {len(files_to_include)} total files")
        
        # Generate and display tree
        tree_text = generate_project_tree(files_to_include, project_root)
        self.menu.display_header("Project Tree Preview")
        print(tree_text)
        print("=" * 50)
        
        # Offer to save
        save = input("\nSave to file? (Y/n): ").strip().lower()
        if save != 'n':
            while True:
                filename = input("Filename (Enter for '.doc-gen/PROJECT_STRUCTURE.txt'): ").strip()
                if not filename:
                    filename = ".doc-gen/PROJECT_STRUCTURE.txt"
                
                # Check for directory-only inputs before expanding
                if filename in ['~', '~/', '.', './'] or filename.endswith('/'):
                    print(f"\n✗ '{filename}' is a directory path, not a filename")
                    print("Please specify a filename, e.g., '~/ PROJECT_STRUCTURE.txt' or '.doc-gen/PROJECT_STRUCTURE.txt'")
                    retry = input("Try again? (Y/n): ").strip().lower()
                    if retry == 'n':
                        break
                    continue
                
                # Expand user path (~ to /home/user)
                filepath = Path(filename).expanduser().resolve()
                
                # Check if it's an existing directory
                if filepath.exists() and filepath.is_dir():
                    print(f"\n✗ '{filename}' is a directory, not a file")
                    print(f"Please specify a filename, e.g., '{filepath}/PROJECT_STRUCTURE.txt'")
                    retry = input("Try again? (Y/n): ").strip().lower()
                    if retry == 'n':
                        break
                    continue
                
                # Check if parent directory exists or can be created
                try:
                    filepath.parent.mkdir(parents=True, exist_ok=True)
                except PermissionError:
                    print(f"\n✗ Permission denied: Cannot create directory {filepath.parent}")
                    retry = input("Try a different path? (y/N): ").strip().lower()
                    if retry != 'y':
                        break
                    continue
                except Exception as e:
                    print(f"\n✗ Error creating directory: {e}")
                    retry = input("Try a different path? (y/N): ").strip().lower()
                    if retry != 'y':
                        break
                    continue
                
                # Try to save the file
                save_result = save_project_tree(files_to_include, project_root, str(filepath))
                
                # Verify the file actually exists
                if filepath.exists():
                    print(f"\n✓ Project tree saved to {filepath}")
                    break
                else:
                    print(f"\n✗ Failed to create file: {save_result.get('message', 'Unknown error')}")
                    retry = input("Try a different path? (y/N): ").strip().lower()
                    if retry != 'y':
                        break
        
        input("\nPress Enter to continue...")
    
    # Settings Menu Actions
    
    def view_config(self):
        """Display current configuration with pagination."""
        self.menu.clear_screen()
        self.menu.display_header("Current Configuration")
        print(f"Config file: {self.menu.current_config}\n")
        
        # Load config
        result = load_config(self.menu.current_config)
        
        if result['success']:
            # Format config as string
            config_text = f"Configuration from: {Path(self.menu.current_config).resolve()}\n\n"
            config_text += yaml.dump(result['config'], default_flow_style=False, sort_keys=False)
            
            # Use pager (like 'less')
            pydoc.pager(config_text)
        else:
            print(f"Error loading config: {result['message']}")
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