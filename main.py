import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# draft
import base64
from email.message import EmailMessage
import google.auth

import google.auth

'''
TODO
 SCOPE- readjust at OauthScreen
 https://cloud.google.com/sdk/docs/install - install for AUTH Google Cloud Access
 https://cloud.google.com/sdk/docs/authorizing -authorize
 Commands:
 gcloud init
 gcloud auth application-default login
 pip install google-cloud-language

'''

# https://developers.google.com/gmail/api/auth/scopes
SCOPES = ["https://mail.google.com/"]

CLIENT_SECRET_FILE = "client_secret_dinhthomtest.json"
# Creating current PATH for JSON API Secret JSON
cwd = os.getcwd()
CLIENT_SECRET_FILE_PATH = f"{cwd}/{CLIENT_SECRET_FILE}"
credentials = None


def auth():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        results = service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])

        if not labels:
            print("No labels found.")
            return
        print("Labels:")
        for label in labels:
            print(label["name"])

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")

    return creds


def gmail_read_emails_id(creds):
    """Create and insert a draft email.
   Print the returned draft's message and id.
   Returns: Draft object, including draft id and message meta data.

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """

    try:
        # create gmail api service
        service = build("gmail", "v1", credentials=creds)

        # Get a list of message IDs
        results = service.users().messages().list(userId='me', maxResults=10).execute()
        messages = results.get('messages', [])

        if not messages:
            print('No messages found.')

        else:
            print('Message IDs:')
            for message in messages:
                print(message['id'])



    except HttpError as error:
        print(f"An error occurred: {error}")
        draft = None


def get_gmail_emails_v2(creds, query_string: str):
    service = build("gmail", "v1", credentials=creds)

    results = service.users().messages().list(userId='me', q=query_string, maxResults=10).execute()
    messages = results.get('messages', [])
    if not messages:
        print('No messages found.')
    else:
        print('Messages:')
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            print(f"Message snippet: {msg['snippet']}")


def main():
    # token
    credentials = auth()
    gmail_read_emails_id(credentials)
    get_gmail_emails_v2(credentials, "before:2025/01/01")
    print("Hello!")


if __name__ == "__main__":
    main()
