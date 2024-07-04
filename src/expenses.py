import datetime
import os.path
from rich import print
from rich.console import Console
from rich.theme import Theme
import sys

console = Console()
custom_theme = Theme({"success": "green", "error": "red"})
error = Console(theme=custom_theme)

class ExpenseTracker:
    def __init__(self, name, amount, date, category):
        self.name = name
        self.amount = amount
        self.date = date
        self.category = category

    def __repr__(self):
        return f"{self.name}, {self.amount:.2f}, {self.date}, {self.category}"



def add_expense_category(expense_name, expense_amount, expense_date):
    categories_expense = [
        "Food",
        "Bills",
        "Rent",
        "Car",
        "Education",
        "Miscellaneous"
    ]

    while True:
        console.print(
            "[bold yellow]Select a category from the following options: [/]")
        for i, category in enumerate(categories_expense):
            error.print(f"{i + 1}. {category}", style="success")

        user_select = int(input("Your chosen category number? "))

        if user_select not in range(1, (len(categories_expense) + 1)):
            error.print("Please select a valid category number: ",
                        style="error")
            continue

        else:
            error.print(
                f"You have selected {user_select}: {categories_expense[user_select - 1]} ", style="success")
            category_selection = categories_expense[(user_select) - 1]
            new_expense_object = ExpenseTracker(
                name=expense_name, amount=expense_amount, category=category_selection, date=expense_date)
            return new_expense_object


def add_expense_date():
    while True:
        expense_date = (input("Please enter a date in format YYYY-MM-DD: "))
        if datetime.date.fromisoformat(expense_date):
            error.print(f"You have entered {expense_date}", style="success")
            return expense_date
        else:
            error.print(
                "Invalid date entered, please enter a valid date!", style="error")
            continue


def add_expense_name():
    while True:
        expense_name = input("Please enter an expense name: ")
        if expense_name.isalpha() and (20 >= len(expense_name) > 0):
            error.print(f"You have entered {expense_name}", style="success")
            expense_name = expense_name.capitalize()
            return expense_name
        else:
            error.print("Please type a valid name", style="error")
            continue


def save_expense(new_expense_object: ExpenseTracker, file_path):
    error.print(
        f"Saving your expense.... {new_expense_object} to {file_path}", style="success")
    with open(file_path, "a+") as f:
        f.write(f"{new_expense_object.name}, {new_expense_object.amount:.2f}, {new_expense_object.date}, {new_expense_object.category}\n")


def add_expense_amount():
    while True:
        expense_amount = float(input("Please enter an expense amount: "))
        if expense_amount <= 0:
            error.print(
                "You cannot have an expense amount 0 or lower Please try again: ", style="error")
            continue
        else:
            error.print(
                f"You have entered {expense_amount:.2f}", style="success")
            return expense_amount


def view_expenses(file_path):
    if os.path.exists(file_path):
        while True:
            view_expense = input(
                "Would you like to view your expense entries? (yes/no): ")
            if view_expense.lower() == "yes":
                with open("expenses_list.csv", "r") as f:
                    expense_list = f.readlines()
                    for i, expense in enumerate(expense_list):
                        print(f"{i+1}. {expense}".strip())

                    exit_program()

            elif view_expense.lower() == "no":
                error.print(
                    "You have selected not to view your entries!", style="error")
                return

            else:
                error.print("Please enter a valid answer", style="error")
    else:
        error.print("You currently have no expense entries", style="error")


def total_expenses(file_path, user_budget):
    if os.path.exists(file_path):
        expenses: list[ExpenseTracker] = []
        with open(file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                expense_name, expense_amount, expense_date, expense_category = line.strip().split(",")
                total_expense_object = ExpenseTracker(name=expense_name, amount=float(
                    expense_amount), date=expense_date, category=expense_category)
                expenses.append(total_expense_object)

            amount_by_category = {}
            for expense in expenses:
                key = expense.category
                if key in amount_by_category:
                    amount_by_category[key] += expense.amount
                else:
                    amount_by_category[key] = expense.amount

            for key, value in amount_by_category.items():
                error.print(f"\n   {key} ${value:.2f}", style="success")

            spending_total = sum([expense.amount for expense in expenses])
            error.print(
                f"\nYou have spent a total of: ${spending_total:.2f}", style="success")

            remaining_budget = user_budget - spending_total
            error.print(
                f"    Your remaining budget: ${remaining_budget:.2f}", style="success")

            exit_program()

    else:
        error.print("You have no expense entries to sum", style="error")

    # Remove files

    # if __name__ == "__main__":
    #     main()


def remove_expense(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                print(f"{i+1}. {line}".strip())
            user_delete = int(
                input("Which expense entry would you like to delete? "))
            with open(file_path, 'w') as f:
                index = 1
                for line in lines:
                    if index != user_delete:
                        f.write(line)

                    else:
                        error.print(
                            f"You have successfully deleted entry {user_delete}", style="success")

                    index += 1

        exit_program()

    else:
        error.print(
            "You do not currently have any expense entries to remove! ", style="error")


def exit_program():
    while True:
        reprompt = input("Would you like to add more expenses? (yes/no): ")
        if reprompt.lower() == "yes":
            return
        elif reprompt.lower() == "no":
            sys.exit("You have exited the program")
        else:
            print("Please input either yes or no")

