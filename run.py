import gspread
from google.oauth2.service_account import Credentials

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
        print("Data provided are to be 6 different data values, separated by commas.")
        print("Example: 11,22,33,44,55,66\n")

        data_str = input("Enter your data values here: ")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid!")
            break
    return sales_data

def validate_data(values):
    """
    This function is to check if there is exactly 6 values in our data
    and to check if all datas can be converted into integers
    """
    try:
        [int(value) for value in values]
        if len(values) !=6:
            raise ValueError(
                f"The data provided is {len(values)}, the required data to be entered has to be 6 values"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please enter 6 values.\n")
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

data = get_sales_data()
sales_data=[int(num) for num in data]
update_sales_worksheet(sales_data)