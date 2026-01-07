import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# NOTE: For automated server environments, consider using a Service Account 
# (google.oauth2.service_account.Credentials) instead of InstalledAppFlow.

class GoogleSheetsService:
    def __init__(self, spreadsheet_id: str):
        self.spreadsheet_id = spreadsheet_id
        self.creds = self.authenticate()
        self.service = build('sheets', 'v4', credentials=self.creds)

    def authenticate(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    os.getenv('GOOGLE_SHEETS_CREDENTIALS_JSON', 'credentials.json'), SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds

    def get_sheet_data(self, range_name: str):
        """
        특정 범위의 시트 데이터를 가져옵니다.
        """
        try:
            sheet = self.service.spreadsheets()
            result = sheet.values().get(spreadsheetId=self.spreadsheet_id,
                                        range=range_name).execute()
            values = result.get('values', [])
            return values
        except HttpError as err:
            print(f"An error occurred: {err}")
            return []

if __name__ == "__main__":
    # service = GoogleSheetsService('YOUR_SPREADSHEET_ID')
    # data = service.get_sheet_data('Sheet1!A1:E')
    # print(data)
    pass
