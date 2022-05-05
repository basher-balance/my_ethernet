import pickle
import os

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# from google.oauth2.credentials import Credentials

from .managed_file import ManagedFile
from .keys import client_secrets_file

user_json = "/home/ucsm/Документы/py/pyss/token.pickle"
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
api_version = "v3"
api_service_name = "youtube"

#    if os.path.exists(user_json):
#        creds = Credentials.from_authorized_user_file(USER_TOKEN_FILE, scopes)
#
#    # If there are no (valid) credentials available, let the user log in.
#    if not creds or not creds.valid:
#
#        if creds and creds.expired and creds.refresh_token:
#            creds.refresh(Request())
#        else:
#            flow = InstalledAppFlow.from_client_secrets_file(APP_TOKEN_FILE, SCOPES)
#            creds = flow.run_local_server(port=0)
#
#        with open(USER_TOKEN_FILE, 'w') as token:
#            token.write(creds.to_json())
credentials = None
if os.path.exists(user_json):
    print("Loading Credentials From File...")
    with ManagedFile(user_json, "rb") as token:
        credentials = pickle.load(token)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            #            print("Refreshing Access Token...")
            #            credentials.refresh(Request())
            #    else:
            print("fetching New Tokens...")
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, scopes
            )
            flow.run_local_server(
                port=8080, prompt="consent", authorization_prompt_message=""
            )
            credentials = flow.credentials
            with ManagedFile(user_json, "wb") as f:
                print("Saving Credentials for Future Use...")
                pickle.dump(credentials, f)
youtube = build(api_service_name, api_version, credentials=credentials)
