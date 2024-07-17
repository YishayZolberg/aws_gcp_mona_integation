import gspread
from oauth2client.service_account import ServiceAccountCredentials

AUTH_FILE_NAME = 'NAME OF THE JSON FILE'


def update_google_sheets(row, col, value):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_name(AUTH_FILE_NAME, scope)

    client = gspread.authorize(creds)

    spreadsheet = client.open('Cloud Costs Report')
    sheet = spreadsheet.worksheet('data')
    sheet.update_cell(row, col, value)

    print("Data inserted successfully!")

