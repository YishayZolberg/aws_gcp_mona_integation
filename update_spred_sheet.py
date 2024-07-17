import gspread
from oauth2client.service_account import ServiceAccountCredentials


def google_get_credentials():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_name('json file name', scope)

    client = gspread.authorize(creds)

    spreadsheet = client.open('Cloud Costs Report')
    return spreadsheet

def update_google_sheets(spreadsheet, row, col, value):
    sheet = spreadsheet.worksheet('data')
    sheet.update_cell(row, col, value)

    print("Data inserted successfully!")

