import pickle
import os

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from .managed_file import ManagedFile
from pys.settings import BASE_DIR


user_json = f"{BASE_DIR}/pyss/token.pickle"
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
api_version = "v3"
api_service_name = "youtube"

credentials = None
if os.path.exists(user_json):
    print("Loading Credentials From File...")
    with ManagedFile(user_json, "rb") as token:
        credentials = pickle.load(token)
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        print("Refreshing Access Token...")
        credentials.refresh(Request())
    else:
        print("fetching New Tokens...")
        client_secrets_file = os.environ.get("YOUTUBE_FILE_TOKENS")
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
