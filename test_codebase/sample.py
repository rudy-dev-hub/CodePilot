"""
Sample code file for testing the AI Dev Copilot.
"""

class Calculator:
    def __init__(self):
        self.result = 0

    def add(self, a, b):
        """Add two numbers."""
        self.result = a + b
        return self.result

    def subtract(self, a, b):
        """Subtract b from a."""
        self.result = a - b
        return self.result

def main():
    calc = Calculator()
    print(calc.add(5, 3))
    print(calc.subtract(10, 4))

if __name__ == "__main__":
    main() 