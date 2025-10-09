
# Run once. It creates an album and prints its ID. 
# Keep the ID and store it in storage_settings.yaml

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def main():
    
    albumname= "Valpevakt"
    creds = Credentials.from_authorized_user_file(".secrets/token.json")

    service = build("photoslibrary", "v1", credentials=creds,static_discovery=False)

    album = service.albums().create(body={"album": {"title": Valpevakt}}).execute()
    print("Created album:", album)

if __name__ == '__main__':
    main()