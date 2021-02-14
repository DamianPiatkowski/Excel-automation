from datetime import datetime

def validate_date(user_input: str) -> bool:
    try:
        datetime.strptime(user_input, "%d/%m/%Y")
        return True
    except ValueError:
        print("Incorrect date format, should be dd/mm/yyyy")
        return False

def collect_user_input(categories: list) -> dict:
    new_row = dict()
    while True:
        new_row["date"] = input("What's the date of this purchase? Please use the format dd/mm/yyyy")
        if validate_date(new_row["date"]):
            break
        else:
            print("Try again")

def main():
    #your main flow, call other functions here
    print("nothing")

if __name__ == "__main__":
    main()