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
            row["date"] = input("What's the date of this purchase? Please use the format dd/mm/yyyy ")
            if validate_date(row["date"]):
                break
            else:
                print("Wrong format, try again")

        while True:
            amount = input("What's the amount? ")
            if amount.isdigit():
                row["amount"] = int(amount)
                break
            else:
                print("Please give just the number ")
        
        while True:
            for count, value in enumerate(categories, start=1):
                print(count, value)
            index = int(input("Choose the category by writing its number "))
            if 1 <= int(index) <= len(categories):
                row["category"] = categories[index-1]
                break
            else:
                print("Please choose one of the available numbers ")
        
        row["description"] = input("Add a short description for this purchase ")
        new_rows.append(row)
        
        while True:
            another_one = input("Done, would you like to add another purchase? yes/no ")
            if another_one.lower() in ["yes", "no"]:
                break
            else:
                print("Something went wrong, answer yes or no")
        if another_one == "no":
            print(f"cool, the following {len(new_rows)} row(s) will be saved:")
            for row in new_rows:
                print(row)
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

def get_stats_options() -> list:
    workbook = load_workbook(filename=file_path)
    sheet = workbook.active
    options = []
    for row in sheet.iter_rows(min_row=2,min_col=1, max_col=4, values_only=True):
        month_year = datetime.strftime(row[0], "%m/%y")
        if month_year not in options:
            options.append(month_year) 
    #add here printing message to user
    # Sort chronologically in case the user did not feed excel with dates in chronological order 
    options.sort(key= lambda date: datetime.strptime(date, "%m/%y"))
    return options

def get_user_request(stats_options: list) -> list:  
    print("You can get summary for the following months:")
    for option in stats_options:
        print(option)
    user_choices = []
    while True:
        answer = input("Would you like to see statistics for any of these months? yes/no ")
        if answer.lower() == "no":
            return user_choices
        elif answer.lower() == "yes":
            break
        else:
            print("Something went wrong, only yes or no answers are valid, try again")
    
    while True:
        while True:
            option_chosen = input("Write what option in format mm/YY, for example 01/20 for January 2020 ")
            if option_chosen in stats_options and option_chosen not in user_choices:
                user_choices.append(option_chosen)
                print(option_chosen + "added to your request")
                break
            else:
                print("your chosen option is not on the list or you've added it already, please try again")
                for option in stats_options:
                    print(option)
        
        while True:
            print("So far you have requested statistics for these months:")
            for option in user_choices:
                print(option)
            want_quit = input("Would you like to add another month to your request? yes/no ")
            if want_quit.lower() == "no":
                return user_choices
            elif want_quit.lower() == "yes":
                break
            else:
                print("Something went wrong, try again: yes/no")
    return user_choices    

def get_stats_data(categories: list, user_choices: list) -> list:
    workbook = load_workbook(filename=file_path)
    sheet = workbook.active
    stats_data = []
    for month in user_choices:
        new_dict = {}
        new_dict["month"] = month
        new_dict["total"] = 0
        all_transactions = []
        for row in sheet.iter_rows(min_row=2,min_col=1, max_col=4, values_only=True):
            if month == datetime.strftime(row[0], "%m/%y"):
                new_dict["total"] += row[1]
                all_transactions.append(row)
        all_transactions.sort(key=lambda x: x[1], reverse=True)
        new_dict["top_5"] = all_transactions[:5]
        new_dict["categories"] = {}
        for category in categories:
            new_dict["categories"][category] = sum([i[1] for i in all_transactions if i[2] == category])
        print(new_dict)
        




#def print_stats(stats_data: list):

#def plot(stats_data):

def main():
    new_rows = collect_user_input(categories)
    if os.path.isfile(file_path) == False:
        create_new_excel()
    save_new_rows_to_excel(new_rows)
    stats_options = get_stats_options()
    user_choices = get_user_request(stats_options)
    if user_choices != []:
        stats_data = get_stats_data(categories, user_choices)
        #print_stats(stats_data)
        #if len(user_choices) > 1:
            #plot(user_choices)
    input("Hit the enter to exit. Thanks!")

if __name__ == "__main__":
    main()