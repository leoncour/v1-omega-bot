import sys

def show_menu():
    print("""
🔧 Manual Strategy Trigger Menu
1. Grid Trading
2. VWAP Reversal
3. Break & Retest
4. Hedging
5. Exit
""")

def get_choice():
    return input("Enter choice (1-5): ").strip()