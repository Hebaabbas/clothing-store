import gspread
import sys
from google.oauth2.service_account import Credentials
from pprint import pprint
from datetime import datetime

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
            print("Great! Now you can document the amount of products sold on the end of your business day.")
            return True
        elif store_condition.lower() == "no":
            print("Please come back when the business day is over and you have all the products sold counted.")
            return False
        else:
            print("You did not insert a valid option, please give it another try")
            continue

       
def get_sales_data():
    """
    This function is to give the store a name, specifies the business day date. And its for getting the data values of the sold products.
    """
    
    while True:
        today = datetime.now().date()

        print("Welcome to " + store_name.capitalize() + "'s sales data collector.")
        print("Please enter how many products were sold on the date of " + str(today))
        print("Data provided are to be 5 different data values, separated by commas.")
        print("Data provided represents these products in this order: [shirt, jeans, dress, shoe, bag] and the maximum amount of products per item we can sell each day is 30. ")
        print("Data shold be as this Example: 11,11,11,11,11\n")

        data_str = input("Enter your data values here: ")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid!")
            break
    sales_data = [int(value) for value in sales_data]
    return sales_data

def validate_data(values):
    """
    This function is to check if there is exactly 5 values in our data
    and to check if all datas can be converted into integers.
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

def update_worksheet(data, worksheet):
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} Worksheet is successfully updated")

def calculate_floor_data(sales_row):
    """
    This function will calculate how many products are available on the store floor (still in the store to sell).
    That means it will calculate how many products we have left from our storage (30 max per product) after our selling business day.
    """
    print("Calculating products on the store floor..\n")
    storage = 30
    floor_data =[]
    for sales in sales_row:
        floor = storage - sales
        floor_data.append(floor)
    return floor_data

def calculate_refill_data(floor, storage):
    refill_count = storage - sum(floor)
    return refill_count if refill_count > 0 else 0      


def main():
    store = store_ready()
    data = get_sales_data()
    if validate_data(data):
        sales_data = [int(num) for num in data]
        update_worksheet(sales_data, "sales")
        floor_data = calculate_floor_data(sales_data)
        update_worksheet(floor_data, "floor")
        refill_count = calculate_refill_data(floor_data, 150)
        print(f"{refill_count} products need to be refilled for tomorrow")
        print("Thank you for using our system.")


main()
