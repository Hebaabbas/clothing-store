import gspread
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

def get_sales_data():
    """
    Get sales values input from the user
    """
    while True:
        print("Welcome to the clothing store sales data collector.")
        print("Please enter the sales data from the last sales day.")
        print("Data provided are to be 5 different data values, separated by commas.")
        print("Example: 11,22,33,44,55\n")

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
                f"The data provided is {len(values)}, the required data to be entered has to be 6 values"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please enter 5 values.\n")
        return False

    return True
   
def update_sales_worksheet(data):
    """
    Updates sales values in the worksheet as well as it adds new row with the new added values
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Worksheet is successfully updated.\n")

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
    print(storage_row)


def main():
    data = get_sales_data()
    sales_data=[int(num) for num in data]
    update_sales_worksheet(sales_data)
    calculate_floor_data(sales_data)

main()
