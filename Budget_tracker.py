import csv
import os
from datetime import datetime

BUDGET_FILE = "budget.txt"
EXPENSE_FILE = "expenses.csv"

def init_files():
    if not os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, "w") as f:
            f.write("0.00")
    if not os.path.exists(EXPENSE_FILE):
        with open(EXPENSE_FILE, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "amount", "category", "note"])

def get_budget():
    try:
        with open(BUDGET_FILE, "r") as f:
            return float(f.read().strip())
    except:
        return 0.0

def set_budget():
    try:
        new_budget = float(input("Enter your monthly budget in $: "))
        with open(BUDGET_FILE, "w") as f:
            f.write(f"{new_budget:.2f}")
        print(f"✅ Budget set to ${new_budget:.2f}")
    except ValueError:
        print("❌ Invalid input. Try again.")

def add_expense():
    try:
        amount = float(input("Enter amount spent ($): "))
        category = input("Enter category (Food, Travel, etc): ")
        note = input("Optional note: ")
        date = datetime.now().strftime("%Y-%m-%d")
        with open(EXPENSE_FILE, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([date, amount, category, note])
        print("✅ Expense added.")
    except ValueError:
        print("❌ Invalid amount.")

def total_spent():
    spent = 0
    if os.path.exists(EXPENSE_FILE):
        with open(EXPENSE_FILE, mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    spent += float(row["amount"])
                except:
                    continue
    return spent

def view_budget_status():
    budget = get_budget()
    spent = total_spent()
    remaining = budget - spent

    print(f"\n💵 Budget: ${budget:.2f}")
    print(f"💸 Spent:  ${spent:.2f}")
    if remaining >= 0:
        print(f"✅ Remaining: ${remaining:.2f}\n")
    else:
        print(f"⚠️ Over Budget by: ${abs(remaining):.2f}\n")

def view_summary():
    if not os.path.exists(EXPENSE_FILE):
        print("No expenses found.")
        return

    print("\n📊 Expense Summary:")
    category_totals = {}
    with open(EXPENSE_FILE, mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            category = row["category"]
            try:
                amount = float(row["amount"])
                category_totals[category] = category_totals.get(category, 0) + amount
            except:
                continue

    for cat, amt in category_totals.items():
        print(f" - {cat}: ${amt:.2f}")
    print()

def show_menu():
    print("""
===========================
💼 Personal Budget Tracker
===========================
1. Set Monthly Budget
2. Add an Expense
3. View Budget Status
4. View Spending Summary
5. Exit
""")

def main():
    init_files()
    while True:
        show_menu()
        choice = input("Select an option (1-5): ").strip()
        if choice == "1":
            set_budget()
        elif choice == "2":
            add_expense()
        elif choice == "3":
            view_budget_status()
        elif choice == "4":
            view_summary()
        elif choice == "5":
            print("👋 Exiting. Your data is saved.")
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main()
