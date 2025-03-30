from datetime import datetime

expenses = []
budget = 0.0

def load_expenses():
    global expenses
    file_name = 'expenses.txt'
    print(f"Loading previous expenses from {file_name}")
    try:
        with open(file_name, 'r') as f:
            for line in f:
                date, category, amount, description = line.strip().split(',')
                expenses.append({
                    'date': date,
                    'category': category,
                    'amount': float(amount),
                    'description': description,
                })
    except FileNotFoundError:
        print('No previous expenses found.')
    except Exception as e:
        print(f'Error loading expenses: {e}')

load_expenses()

def get_valid_date(valid = True):
    date = input('What is the date of the expense? (YYYY-MM-DD)') if valid == True else input('Enter a valid date in the format YYYY-MM-DD')
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return date
    except ValueError:
        return get_valid_date(False)

def get_valid_float(prompt = 'What is the amount?', valid = True):
    amount_string = input(prompt)
    try:
        return float(amount_string)
    except (ValueError, TypeError):
        return get_valid_float('Enter a valid amount', False)

def get_valid_string(valid = True, prompt = 'Invalid value, please try again.'):
    value = input(prompt) if valid == True else input(prompt)
    if len(value.strip()) > 0:
        return value.strip()
    else: 
        return get_valid_string(False)

def menu():
    global budget
    
    print("\n--- Main Menu ---")
    print("1. Add an expense")
    print("2. View expenses")
    print("3. Track budget")
    print("4. Save expenses")
    print("5. Exit")
    
    choice = input("Enter your choice: ")

    if choice == "1":
        add_expense()
    elif choice == "2":
        view_expenses()
    elif choice == "3":
        budget = get_valid_float('What is your total budget for the month?', True)
        track_budget(budget)
    elif choice == "4":
        save_expenses()
    elif choice == "5":
        print("Exiting program. Goodbye!")
    else:
        print("Invalid choice. Please try again.")

def save_expenses():
    global expenses
    if len(expenses) == 0:
        print('No expenses to save.')
        menu()
    else:
        with open('expenses.txt', 'w') as f:
            for e in expenses:
                f.write(f"{e['date']},{e['category']},{e['amount']},{e['description']}\n")
        print('Expenses have been saved.')
        menu()   
    

def add_expense():
    global budget
    print("Ok, let's add an expense")
    date = get_valid_date()
    category = get_valid_string(True, 'What is the category of the expense?')
    amount = get_valid_float('What is the amount?', True)
    description = get_valid_string(True, 'Briefly describe the expense.')
    new_expense = {
        'date': date,
        'category': category,
        'amount': amount,
        'description': description,
    }
    expenses.append(new_expense)
    print('Expense has been added.')

    if budget > 0:
        track_budget(budget)
    else:
        prompt_to_add_expense()
        

def prompt_to_add_expense():
    action = input('Would you like to add an expense? (y/n)')
    if (action.lower() == 'y'):
        add_expense()
    else:
        menu()
    

def view_expenses():
    if len(expenses) == 0:
        print('No expenses have been entered yet')
        action = input('Would you like to enter an expense? (y/n)')
        if (action.lower() == 'y'):
            add_expense()
        else:
            menu()
    else:
        print('Expenses')
    
        # Print headers
        print(f"{'Date':<12} {'Category':<12} {'Amount':>8}  Description")
        print("-" * 50)

        # Print rows
        for e in expenses:
            print(f"{e['date']:<12} {e['category']:<12} ${e['amount']:>6.2f}  {e['description']}")

        menu()

# TODO Implement running total instead of loop over all expenses every time.
def track_budget(budget):
    total_spent = 0
    for expense in expenses:
        total_spent += expense['amount']
    if(total_spent > budget):
        print(f"You have exceeded your budget by {total_spent - budget}")
    else: 
        print(f"You have {budget - total_spent} left for the month")
    
    prompt_to_add_expense()
        

menu()
