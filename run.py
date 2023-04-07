import gspread
import sys
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('clothing_store')

store_name = input("Hello! This is a clothing store data collector. First, please input the name of the clothing store you'd like to run: ")
user_age= int(input("And now please input your age: "))
if user_age < 18:
    raise SystemExit('The user must be at least 18')
            
def store_ready():       
    while True:
        store_condition = input("Is the business day over now and you have all the products you've sold counted? please insert yes or no: ")
        if store_condition.lower() == "yes":
            print("Great! Now you can document the amount of products sold.")
            break
        elif store_condition.lower() == "no":
            print("Please come back when the business day is over and you have all the products sold counted.")
            sys.exit()
        else:
            print("You did not insert a valid option, please give it another try")
            continue

       
def get_sales_data():
    """
    Get sales values input from the user
    """
    while True:


        print("Welcome to " + store_name.capitalize() + "'s sales data collector.")
        print("Please enter how many products were sold the last business day.")
        print("Data provided are to be 5 different data values, separated by commas.")
        print("Data provided represents these products in this order: [shirt, jeans, dress, shoe, bag]")
        print("Data shold be as this Example: 11,22,33,44,55\n")

        data_str = input("Enter your data values here: ")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid!")
            break
    return sales_data

def validate_data(values):
    """
    This function is to check if there is exactly 5 values in our data
    and to check if all datas can be converted into integers
    """
    try:
        [int(value) for value in values]
        if len(values) !=5:
            raise ValueError(
                f"The data provided is {len(values)}, the required data to be entered has to be 5 values"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please enter 5 values.\n")
        return False

    return True
   

def calculate_sales_worksheet(data):
    """to calculate how many products in total we sold at the end of the day"""
    print("Calculating our sales...\n")
    total_sales = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales-Worksheet is successfully updated.\n")
"""
def update_floor_worksheet(data):
    "Updates floor values in the worksheet as well as it adds new row with the new added values"
    print("Updating floor worksheet...\n")
    floor_worksheet = SHEET.worksheet("floor")
    floor_worksheet.append_row(data)
    print("Floor-Worksheet is successfully updated.\n")
"""

def update_worksheet(data, worksheet):
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} Worksheet is successfully updated")

def calculate_floor_data(sales_row):
    """
    This function will calculate how many products are available on the store floor.
    That means it will calculate how many products we took from our storage to refill the store and
    how many products that we havent sold and still on our store floor.
    A positive number means the number of products that was extra out in the store, not sold
    A negative number means the number of products that we had to get from the storage in order to refill the store.
    """
    print("Calculating products on the store floor..\n")
    storage = SHEET.worksheet("storage").get_all_values()
    storage_row = storage[-1]

    floor_data =[]
    for storage, sales in zip(storage_row, sales_row):
        floor = int(storage) - sales
        floor_data.append(floor)
    return floor_data


def main():
    store = store_ready()
    data = get_sales_data()
    sales_data=[int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_floor_data = calculate_floor_data(sales_data)
    update_worksheet(new_floor_data, "floor")
    storage_data= calculate_storage_data(storage_row)
    update_worksheet(storage_data, "storage")

main()
