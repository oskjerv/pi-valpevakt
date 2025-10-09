# Must be run with screen. 
# Cannot be run headlessly.
# Use for example VNC Viewer

from google_auth_oauthlib.flow import InstalledAppFlow
import json

# Scopes: include 'photoslibrary.appendonly' for upload access
SCOPES = ["https://www.googleapis.com/auth/photoslibrary.appendonly"]

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
