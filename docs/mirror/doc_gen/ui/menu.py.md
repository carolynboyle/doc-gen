# menu.py

**Path:** doc_gen/ui/menu.py
**Syntax:** python
**Generated:** 2026-01-03 17:24:45

```python
"""
Menu system for doc-gen documentation generator.
Provides interactive menu-driven interface with placeholder functions.
"""

from doc_gen.core.config import initialize_config as init_config, load_config
import yaml


class MenuSystem:
    """Interactive menu system using dispatch dictionary pattern."""
    
    def __init__(self):
        """Initialize menu system with dispatch mappings."""
        self.running = True
        self.current_config = "doc-config.yml"  # Default config path
        
        # Main menu dispatch dictionary
        self.main_menu_actions = {
            '1': self.interactive_mode,
            '2': self.generate_docs,
            '3': self.check_mode,
            '4': self.initialize_config,
            '5': self.settings_menu,
            '6': self.exit_program
        }
        
        # Settings submenu dispatch dictionary
        self.settings_actions = {
            '1': self.view_config,
            '2': self.edit_config_path,
            '3': self.view_plugins,
            '4': self.back_to_main
        }
    
    def display_header(self, title):
        """Display formatted section header."""
        print(f"\n{'=' * 50}")
        print(f"{title:^50}")
        print('=' * 50)
    
    def display_main_menu(self):
        """Display main menu options."""
        self.display_header("Doc-Gen Documentation Generator")
        print(f"Config: {self.current_config}\n")
        print("1. Interactive Mode - Scan project and build manifest")
        print("2. Generate Documentation - From existing manifest")
        print("3. Check Mode - Dry run (show what would change)")
        print("4. Initialize Config - Create doc-config.yml template")
        print("5. Settings")
        print("6. Exit")
        print()
    
    def display_settings_menu(self):
        """Display settings submenu options."""
        self.display_header("Settings")
        print("1. View Current Configuration")
        print("2. Edit Configuration Path")
        print("3. View Plugin Status")
        print("4. Back to Main Menu")
        print()
    
    def get_choice(self, valid_choices):
        """
        Get and validate user menu choice.
        
        Args:
            valid_choices: Set of valid choice strings
            
        Returns:
            str: Valid user choice
        """
        while True:
            try:
                choice = input("Enter choice: ").strip()
                if choice in valid_choices:
                    return choice
                print(f"Invalid choice. Please enter {', '.join(sorted(valid_choices))}")
            except (KeyboardInterrupt, EOFError):
                print("\n\nExiting...")
                return '6'  # Exit choice
    
    # Main Menu Actions
    
    def interactive_mode(self):
        """Interactive mode to scan project and build manifest."""
        from doc_gen.core.builder import run_interactive_mode
    
        print("\n" + "=" * 50)
        print("Interactive Mode - Build Manifest")
        print("=" * 50)
    
        # Get project path from user (or use current directory)
        project_path = input("\nProject directory to scan (Enter for current directory): ").strip()
        if not project_path:
            project_path = None  # Will default to current directory
    
        # Run interactive mode
        result = run_interactive_mode(
        project_root=project_path,
        config_path=self.current_config
        )
    
        # Display result
        print(f"\n{result['message']}")
    
        if not result['success']:
            print("(Interactive mode did not complete successfully)")
    
        input("\nPress Enter to continue...")
    



    def generate_docs(self):
        """Generate documentation from existing manifest."""
        from doc_gen.core.builder import run_generate_mode
    
        print("\n" + "=" * 50)
        print("Generate Documentation from Manifest")
        print("=" * 50)
    
        # Get manifest path from user (or use default)
        manifest_path = input("\nManifest file (Enter for 'manifest.yml'): ").strip()
        if not manifest_path:
            manifest_path = "manifest.yml"
    
        # Run generate mode
        result = run_generate_mode(
        manifest_path=manifest_path,
        config_path=self.current_config
        )
        # Display result
    
    
        print(f"\n{result['message']}")
    
        if not result['success']:
            print("(Generation did not complete successfully)")
    
        input("\nPress Enter to continue...")

    def check_mode(self):
        """Placeholder: Dry-run mode to check what would change."""
        print("\n[PLACEHOLDER] Check Mode")
        print("This will show what would be generated without writing files")
        input("\nPress Enter to continue...")
    
    def initialize_config(self):
        """Create configuration template from doc-config.yml.template."""
        print("\nInitializing configuration file...")
        
        # Call the real function from config module
        result = init_config()
        
        # Display the result
        print(f"\n{result['message']}")
        
        if not result['success']:
            print("(Config initialization failed)")
        
        input("\nPress Enter to continue...")
    
    def settings_menu(self):
        """Display and handle settings submenu."""
        while True:
            self.display_settings_menu()
            choice = self.get_choice(self.settings_actions.keys())
            
            # Execute selected action
            action = self.settings_actions[choice]
            result = action()
            
            # Break back to main menu if requested
            if result == 'back':
                break
    
    def exit_program(self):
        """Exit the program gracefully."""
        print("\nExiting doc-gen. Goodbye!")
        self.running = False
    
    # Settings Menu Actions (placeholders)
    
    def view_config(self):
        """Display current configuration."""
        print("\nLoading configuration...")
        
        # Load the config file
        result = load_config(self.current_config)
        
        print(f"\n{result['message']}\n")
        
        if result['success']:
            # Display the config in a readable format
            print("=" * 50)
            print(yaml.dump(result['config'], default_flow_style=False, sort_keys=False))
            print("=" * 50)
        else:
            print("(Unable to load configuration)")
        
        input("\nPress Enter to continue...")
    
    def edit_config_path(self):
        """Placeholder: Change configuration file path."""
        print("\n[PLACEHOLDER] Edit Configuration Path")
        new_path = input(f"Current: {self.current_config}\nEnter new path (or Enter to cancel): ").strip()
        if new_path:
            self.current_config = new_path
            print(f"Configuration path updated to: {self.current_config}")
        input("\nPress Enter to continue...")
    
    def view_plugins(self):
        """Placeholder: Show plugin status."""
        print("\n[PLACEHOLDER] Plugin Status")
        print("This will show loaded plugins and their status")
        input("\nPress Enter to continue...")
    
    def back_to_main(self):
        """Return to main menu."""
        return 'back'
    
    def run(self):
        """Main menu loop."""
        while self.running:
            self.display_main_menu()
            choice = self.get_choice(self.main_menu_actions.keys())
            
            # Execute selected action
            action = self.main_menu_actions[choice]
            action()


def main():
    """Entry point for standalone menu testing."""
    menu = MenuSystem()
    menu.run()


if __name__ == '__main__':
    main()
```
