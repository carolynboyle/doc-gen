"""
Menu system for doc-gen documentation generator.
Provides interactive menu-driven interface.
"""

from pathlib import Path
import sys
import os

# Ensure .doc-gen/ structure exists before anything else
from doc_gen.core.config import ensure_doc_gen_structure, DEFAULT_CONFIG_PATH

result = ensure_doc_gen_structure()
if not result['success']:
    print("\n" + "=" * 60)
    print("❌ ERROR: Cannot create .doc-gen/ directory")
    print("=" * 60)
    print(f"\n{result['message']}")
    print("\nPossible causes:")
    print("  - Insufficient permissions in current directory")
    print("  - Disk full")
    print("  - Read-only filesystem")
    print("\nPlease fix the issue and try again.")
    print("=" * 60 + "\n")
    sys.exit(1)

# Check for virtual environment
if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    print("\n" + "=" * 60)
    print("⚠️  ERROR: Virtual environment not activated!")
    print("=" * 60)
    print("\nPlease activate the virtual environment first:")
    print("\n  Linux/Mac:  source .venv/bin/activate")
    print("  Windows:    .venv\\Scripts\\activate")
    print("\nThen run the command again.")
    print("=" * 60 + "\n")
    sys.exit(1)

from doc_gen.ui.menu_actions import MenuActions


class MenuSystem:
    """Interactive menu system using dispatch dictionary pattern."""

    def __init__(self):
        """Initialize menu system with dispatch mappings."""
        self.running = True
        self.current_config = str(DEFAULT_CONFIG_PATH)  # Default: .doc-gen/config.yml

        # Create actions handler
        self.actions = MenuActions(self)

        # Main menu dispatch dictionary
        self.main_menu_actions = {
            '1': self.actions.generate_tree,
            '2': self.actions.interactive_mode,
            '3': self.actions.check_mode,
            '4': self.actions.generate_docs,
            '5': self.settings_menu,
            '6': self.exit_program
        }

        # Settings submenu dispatch dictionary
        self.settings_actions = {
            '1': self.actions.view_config,
            '2': self.actions.edit_config_path,
            '3': self.actions.view_plugins,
            '4': self.back_to_main
        }

    def clear_screen(self):
        """Clear the terminal screen."""
        try:
            os.system('clear' if os.name == 'posix' else 'cls')
        except Exception:
            # Future: Replace with logger
            # logger.debug(f"Screen clear failed: {e}")
            pass

    def display_header(self, title):
        """Display formatted section header."""
        print(f"\n{'=' * 50}")
        print(f"{title:^50}")
        print('=' * 50)

    def display_main_menu(self):
        """Display main menu options."""
        self.display_header("Doc-Gen Documentation Generator")
        print(f"Config: {self.current_config}\n")
        print("1. Generate Project Tree - Create structure visualization")
        print("2. Scan Project - Select files to document")
        print("3. Check Mode - Dry run (show what will be created)")
        print("4. Generate Documentation - From selected files")
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