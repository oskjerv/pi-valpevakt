# Must be run with screen. 
# Cannot be run headlessly.
# Use for example VNC Viewer

from google_auth_oauthlib.flow import InstalledAppFlow
import json

# Scopes:
# - appendonly: upload (create) media and add to albums
# - readonly.appcreateddata: list/search media and albums created by this app (for deleter)
# - edit.appcreateddata: remove media from albums created by this app (for deleter)
SCOPES = [
    "https://www.googleapis.com/auth/photoslibrary.appendonly",
    "https://www.googleapis.com/auth/photoslibrary.readonly.appcreateddata",
    "https://www.googleapis.com/auth/photoslibrary.edit.appcreateddata",
]

def main():
    flow = InstalledAppFlow.from_client_secrets_file(
        ".secrets/credentials.json", SCOPES
    )

    # 'offline' ensures we get a refresh_token
    creds = flow.run_local_server(port=8080, access_type='offline', prompt='consent')

    with open(".secrets/token.json", "w") as token:
        token.write(creds.to_json())

    print("✅ New token.json created with refresh_token")

if __name__ == "__main__":
    main()
