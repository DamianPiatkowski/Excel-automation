from datetime import datetime

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
            row["amount"] = input("What's the amount?")
            if row["amount"].isdigit():
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
def main():
    print(collect_user_input(categories))

if __name__ == "__main__":
    main()