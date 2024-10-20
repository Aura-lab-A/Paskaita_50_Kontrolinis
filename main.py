import sqlite3

connection = sqlite3.connect("finances.db")
cursor = connection.cursor()

create_table = '''CREATE TABLE IF NOT EXISTS finances (
    id PRIMARY KEY NOT NULL,
    type TEXT NOT NULL,
    amount FLOAT NOT NULL,
    category TEXT NOT NULL)'''

with connection:
    cursor.execute(create_table)

# with connection:
#     cursor.execute('''INSERT INTO finances VALUES
#     (1, "Income", 76128, "Car sell"),
#     (2, "Income", 2927, "Salary"),
#     (3, "Income", 916, "Project"),
#     (4, "Income", 700, "Tax return"),
#     (5, "Expenses", 316, "Utilities"),
#     (6, "Expenses", 292, "Groceries"),
#     (7, "Expenses", 53, "Fuel"),
#     (8, "Expenses", 43, "Clothes"),
#     (9, "Expenses", 87, "Dinner"),
#     (10, "Expenses", 85, "Haircut"),
#     (11, "Expenses", 52, "Medicine")''')


def main_menu():
    while True:
        print("\nPersonal Finance Manager")
        print("1. Enter Income")
        print("2. Enter Expense")
        print("3. Get Balance")
        print("4. Get All Incomes")
        print("5. Get All Expenses")
        print("6. Delete Income/Expense")
        print("7. Update Income/Expense")
        print("8. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            enter_income()
        elif choice == '2':
            enter_expenses()
        elif choice == '3':
            get_balance()
        elif choice == '4':
            get_all_incomes()
        elif choice == '5':
            get_all_expenses()
        elif choice == '6':
            delete_record()
        elif choice == '7':
            update_record()
        elif choice == '8':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")


def add_record(id, type, amount, category):
    with connection:
        cursor.execute("INSERT INTO finances VALUES(?,?,?,?)", (id, type, amount, category))


def enter_income(type="Income"):
    with connection:
        cursor.execute("SELECT MAX(id) FROM finances")
        result = cursor.fetchall()
        id = result[0][0] + 1
    amount = float(input("Enter amount of the income: "))
    category = input("Enter category of the income: ")
    add_record(id, type, amount, category)
    print("The income is recorded!")


def enter_expenses(type="Expenses"):
    with connection:
        cursor.execute("SELECT MAX(id) FROM finances")
        result = cursor.fetchall()
        id = result[0][0] + 1
    amount = float(input("Enter amount of the expenses: "))
    category = input("Enter category of the expenses: ")
    add_record(id, type, amount, category)
    print("The expenses are recorded!")


def get_balance():
    with connection:
        cursor.execute('''SELECT SUM(amount) FROM finances WHERE type = "Income"''')
        sum_income = cursor.fetchall()
        cursor.execute('''SELECT SUM(amount) FROM finances WHERE type = "Expenses"''')
        sum_expenses = cursor.fetchall()
        result = sum_income[0][0] - sum_expenses[0][0]
        print(f"The current balance is: {result} EUR")


def get_all_incomes():
    with connection:
        cursor.execute('''SELECT * FROM finances WHERE type = "Income"''')
        result = cursor.fetchall()
        print(f"The income records: {result}")


def get_all_expenses():
    with connection:
        cursor.execute('''SELECT * FROM finances WHERE type = "Expenses"''')
        result = cursor.fetchall()
        print(f"The expenses records: {result}")


def delete_query(type=None, amount=None, category=None):
    query = "DELETE FROM finances WHERE 1=1"
    parameters = []
    if type:
        query += " AND type=?"
        parameters.append(type)
    if amount:
        query += " AND amount=?"
        parameters.append(amount)
    if category:
        query += " AND category=?"
        parameters.append(category)
    # print(query)
    with connection:
        cursor.execute(query, parameters)
        print("Deletion has been completed.")


def delete_record():
    type = input("Enter record type (or leave blank): ")
    amount = input("Enter record amount (or leave blank): ")
    category = input("Enter record category (or leave blank): ")
    if type == "" and amount == "" and category == "":
        question = input(f"Are you sure you want to delete all records? Please answer (y/n): ")
        if question == "y":
            delete_query(type=type if type else None,
                         amount=amount if amount else None,
                         category=category if category else None)
        if question == "n":
            print("Please select another criterion.")
    else:
        delete_query(type=type if type else None,
                     amount=amount if amount else None,
                     category=category if category else None)


def update_query(type=None, amount=None, category=None, n_type=None, n_amount=None, n_category=None):
    query = "UPDATE finances SET "
    parameters = []
    if n_type:
        query += "type=?"
        parameters.append(n_type)
    if n_type and n_amount:
        query += ", amount=?"
        parameters.append(n_amount)
    if n_type is None and n_amount:
        query += "amount=?"
        parameters.append(n_amount)
    if n_type and n_category:
        query += ", category=?"
        parameters.append(n_category)
    if n_amount and n_category:
        query += ", category=?"
        parameters.append(n_category)
    if n_type is None and n_amount is None and n_category:
        query += "category=?"
        parameters.append(n_category)
    query += " WHERE 1=1"
    if type:
        query += " AND type=?"
        parameters.append(type)
    if amount:
        query += " AND amount=?"
        parameters.append(amount)
    if category:
        query += " AND category=?"
        parameters.append(category)
    # print(query)
    with connection:
        cursor.execute(query, parameters)
        print("Update has been completed.")


def update_record():
    type = input("Enter record type to be updated (or leave blank): ")
    amount = input("Enter record amount to be updated (or leave blank): ")
    category = input("Enter record category to be updated (or leave blank): ")
    if type == "" and amount == "" and category == "":
        question1 = input(f"Are you sure you want to update all records? Please answer (y/n): ")
        if question1 == "y":
            n_type = input("Enter new record type (or leave blank): ")
            n_amount = input("Enter new record amount (or leave blank): ")
            n_category = input("Enter new record category (or leave blank): ")
            if n_type == "" and n_amount == "" and n_category == "":
                print("No new values were provided.")
            else:
                update_query(type=type if type else None,
                             amount=amount if amount else None,
                             category=category if category else None,
                             n_type=n_type if n_type else None,
                             n_amount=n_amount if n_amount else None,
                             n_category=n_category if n_category else None)
        if question1 == "n":
            print("Please select more criteria.")
    else:
        n_type = input("Enter new record type (or leave blank): ")
        n_amount = input("Enter new record amount (or leave blank): ")
        n_category = input("Enter new record category (or leave blank): ")
        update_query(type=type if type else None,
                     amount=amount if amount else None,
                     category=category if category else None,
                     n_type=n_type if n_type else None,
                     n_amount=n_amount if n_amount else None,
                     n_category=n_category if n_category else None)



if __name__ == "__main__":
    main_menu()

