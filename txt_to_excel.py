from __future__ import print_function


import os.path
from time import sleep

from google.auth.transport.requests import Request
from pprint import pprint
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1jRWnxGwDauOwYvpXE8LLAm4uqfBpCYiLp79lmroFoHQ'
SAMPLE_RANGE_NAME = 'A:C'


def main(data_file_path):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('tokens.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    tem= [str(a) for a in range(0, 300)]

    while True:
        try:
            service = build('sheets', 'v4', credentials=creds)


            file = open(data_file_path, 'rb')
            data = file.readlines()
            file.close()
            # print(data)
            cleaned_data = []
            for i in data:
                # print(i, type(i))
                cleaned_data.append('')
                for j in str(i):
                    if str(j) in '1234567890 ':
                        cleaned_data[-1] += str(j)
            data = [["X_angle","Y_angle","Z_angle"]]
            for i in cleaned_data:
                # print(i)
                if len(i) > 15:
                    continue
                j = i.split("  ")
                if len(j) == 3 and j[0] in tem and j[1] in tem and j[2] in tem:
                    data.append(j)



            # How the input data should be interpreted.
            value_input_option = 'RAW'  # TODO: Update placeholder value.


            value_range_body={
                "values": data
            }

            request = service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME, valueInputOption=value_input_option,body=value_range_body)
            response = request.execute()

            # TODO: Change code below to process the `response` dict:
            pprint(response)

        except HttpError as err:
            print(err)
        sleep(5)

if __name__ == '__main__':
    main('C:\\Users\\MANAV\\Downloads\\CoolTermWin64Bit\\CoolTermWin64Bit\\best.txt')