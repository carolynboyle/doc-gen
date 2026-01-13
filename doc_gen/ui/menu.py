"""
Menu system for doc-gen documentation generator.
Provides interactive menu-driven interface.
"""

from pathlib import Path
import sys
import os
from doc_gen.core.config import ensure_doc_gen_structure, DEFAULT_CONFIG_PATH
from doc_gen.ui.menu_actions import MenuActions

# Ensure .doc-gen/ structure exists before anything else
result = ensure_doc_gen_structure()
if not result['success']:
    print("\n" + "=" * 60)
    print("ERROR: Cannot create .doc-gen/ directory")
    print("=" * 60)
    print(f"\n{result['message']}")
    print("\nPossible causes:")
    print("  - Insufficient permissions in current directory")
    print("  - Disk full")
    print("  - Read-only filesystem")
    print("\nPlease fix the issue and try again.")
    print("=" * 60 + "\n")
    sys.exit(1)


class MenuSystem:
    """Interactive menu system using dispatch dictionary pattern."""
    
    def __init__(self):
        """Initialize menu system with dispatch mappings."""
        self.running = True
        self.current_config = ".doc-gen/config.yml"  # Default config path
        
        # Create actions handler (needs self reference for menu utilities)
        self.actions = MenuActions(self)
        
        # Main menu dispatch dictionary
        self.main_menu_actions = {
            '1': self.actions.get_project_tree,
            '2': self.actions.scan_project,
            '3': self.actions.check_mode,
            '4': self.actions.generate_docs,
            '5': self.settings_menu,
            '6': self.exit_program
        }
        
        # Settings submenu dispatch dictionary
        self.settings_actions = {
            '1': self.actions.initialize_config,
            '2': self.actions.view_config,
            '3': self.actions.edit_config_path,
            '4': self.actions.manage_ignore_patterns,
            '5': self.actions.view_plugins,
            '6': self.back_to_main
        }
    
    def clear_screen(self):
        """Clear the terminal screen."""
        try:
            os.system('clear' if os.name == 'posix' else 'cls')
        except Exception:
            # Silently fail if screen clear doesn't work
            pass
    
    def display_header(self, title):
        """Display formatted section header."""
        print(f"\n{'=' * 60}")
        print(f"{title:^60}")
        print('=' * 60)
    
    def display_main_menu(self):
        """Display main menu options."""
        self.display_header("Doc-Gen Documentation Generator")
        print(f"Config: {self.current_config}\n")
        print("1. Get Project Filesystem Tree")
        print("2. Scan Project - Select files to document")
        print("3. Check Mode - Dry run (show what will be created)")
        print("4. Generate Documentation - From selected files")
        print("5. Settings")
        print("6. Exit")
        print()
    
    def display_settings_menu(self):
        """Display settings submenu options."""
        self.display_header("Settings")
        print("1. Initialize Config - Create .doc-gen/config.yml template")
        print("2. View Current Configuration")
        print("3. Edit Configuration Path")
        print("4. Manage Ignore Patterns")
        print("5. View Plugin Status")
        print("6. Back to Main Menu")
        print()
    
    def get_choice(self, valid_choices, menu_display_func):
        """
        Get and validate user menu choice.
        
        Args:
            valid_choices: Set of valid choice strings
            menu_display_func: Function to redisplay menu on error
            
        Returns:
            str: Valid user choice
        """
        while True:
            try:
                choice = input("Enter choice: ").strip()
                if choice in valid_choices:
                    return choice
                
                # Invalid input - clear screen, redisplay menu, show error
                self.clear_screen()
                menu_display_func()
                max_choice = max(int(c) for c in valid_choices)
                print(f"Please select an option (1-{max_choice}):\n")
                
            except (KeyboardInterrupt, EOFError):
                print("\n\nExiting...")
                return list(valid_choices)[-1]  # Return last option (Exit)
    
    def settings_menu(self):
        """Display and handle settings submenu."""
        while True:
            self.clear_screen()
            self.display_settings_menu()
            choice = self.get_choice(self.settings_actions.keys(), self.display_settings_menu)
            
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
    
    def back_to_main(self):
        """Return to main menu."""
        return 'back'
    
    def run(self):
        """Main menu loop."""
        while self.running:
            self.clear_screen()
            self.display_main_menu()
            choice = self.get_choice(self.main_menu_actions.keys(), self.display_main_menu)
            
            # Execute selected action
            action = self.main_menu_actions[choice]
            action()


def main():
    """Entry point for standalone menu testing."""
    menu = MenuSystem()
    menu.run()


if __name__ == '__main__':
    main()