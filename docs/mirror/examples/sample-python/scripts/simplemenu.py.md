# simplemenu.py

**Path:** examples/sample-python/scripts/simplemenu.py
**Syntax:** python
**Generated:** 2026-01-03 17:24:45

```python
class SimpleMenu:
    def __init__(self):
        # Actions defined AFTER __init__ completes
        # Using both direct references and lambdas
        self.actions = {
            '1': self.say_hello,           # No args
            '2': lambda: self.greet("Bob"), # With args
            '3': self.exit_menu            # Returns value
        }
    
    def say_hello(self):
        print("Hello!")
    
    def greet(self, name):
        print(f"Hello, {name}!")
    
    def exit_menu(self):
        return False  # Signal to exit
    
    def run(self):
        while True:
            print("\n1. Say Hello")
            print("2. Greet Bob")
            print("3. Exit")
            
            choice = input("Choice: ").strip()
            
            # Safe dispatch
            action = self.actions.get(choice)
            if action:
                result = action()  # Execute it
                if result is False:  # Check return value
                    break
            else:
                print("Invalid choice!")

# Test it
if __name__ == "__main__":
    menu = SimpleMenu()
    menu.run()
```
