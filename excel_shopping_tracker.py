from datetime import datetime
from openpyxl import Workbook, load_workbook
from openpyxl.styles import PatternFill
import os

file_path = os.path.join(os.environ['USERPROFILE'], 'Desktop/Finances.xlsx')
categories = ["baby", "regular groceries", "game", "car related", "taxi"]

def validate_date(user_input: str) -> bool:
    try:
        datetime.strptime(user_input, "%d/%m/%Y")
        return True
    except ValueError:
        print("Incorrect date format, should be dd/mm/yyyy")
        return False

def collect_user_input(categories: list) -> list:
    new_rows = []
    while True:
        row = dict()
        while True:
            row["date"] = input("What's the date of this purchase? Please use the format dd/mm/yyyy")
            if validate_date(row["date"]):
                break
            else:
                print("Wrong format, try again")

        while True:
            amount = input("What's the amount?")
            if amount.isdigit():
                row["amount"] = int(amount)
                break
            else:
                print("Please give just the number")
        
        while True:
            for count, value in enumerate(categories, start=1):
                print(count, value)
            index = int(input("Choose the category by writing its number"))
            if 1 <= int(index) <= len(categories):
                row["category"] = categories[index-1]
                break
            else:
                print("Please choose one of the available numbers")
        
        row["description"] = input("Add a short description for this purchase")
        new_rows.append(row)
        
        while True:
            another_one = input("Done, would you like to add another purchase? yes/no")
            if another_one.lower() in ["yes", "no"]:
                break
            else:
                print("Something went wrong, answer yes or no")
        if another_one == "no":
            print("cool")
            return new_rows


def create_new_excel():
    workbook = Workbook()
    sheet = workbook.active
    sheet["A1"] = "Date"
    sheet["B1"] = "Amount"
    sheet["C1"] = "Category"
    sheet["D1"] = "Description"
    for cell in ["A1", "B1", "C1", "D1"]:
        sheet[cell].fill = PatternFill(start_color="00FF00", patternType="solid")
    workbook.save(filename=file_path)
    workbook.close()

def save_new_rows_to_excel(rows: list):
    workbook = load_workbook(filename=file_path)
    sheet = workbook.active
    current_index = sheet.max_row + 1
    for row in rows:
        sheet["A"+str(current_index)] = datetime.strptime(row['date'], "%d/%m/%Y").date()
        sheet["B"+str(current_index)] = row['amount']
        sheet["C"+str(current_index)] = row['category']
        sheet["D"+str(current_index)] = row['description']
        current_index +=1
    
    workbook.save(filename=file_path)

def show_stats_options() -> list:
    workbook = load_workbook(filename=file_path)
    sheet = workbook.active
    options = []
    for row in sheet.iter_rows(min_row=2,min_col=1, max_col=4, values_only=True):
        month_year = datetime.strftime(row[0], "%m/%y")
        if month_year not in options:
            options.append(month_year) 
    #add here printing message to user
    return options   

def main():
    save_new_rows_to_excel([
                        {'date': '10/01/2021', 'amount': 100, 'category': 'car related', 'description': 'fuel'},
                        {'date': '12/01/2021', 'amount': 23, 'category': 'game', 'description': 'Mario'}, 
                        {'date': '14/01/2021', 'amount': 455, 'category': 'groceries', 'description': 'Auchan'}
                    ])
    print(show_stats_options())
    print(collect_user_input(categories))

if __name__ == "__main__":
    main()