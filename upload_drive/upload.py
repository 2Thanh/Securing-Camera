from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload,MediaIoBaseDownload
import io

# Setup the Drive v3 API
SCOPES = 'https://www.googleapis.com/auth/drive.file'
store = file.Storage('C:\\Users\\vulon\\OneDrive - 2mkhqw\\Desktop\\FireBase\\Flask_detection\\upload_drive\\credentials.json') #Credentials.json get another place with client_secret..json //https://developers.google.com/workspace/guides/create-credentials
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('C:\\Users\\vulon\\OneDrive - 2mkhqw\\Desktop\\FireBase\\Flask_detection\\upload_drive\\client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
drive_service = build('drive', 'v3', http=creds.authorize(Http()))

def uploadFile(file_name):
    file_metadata = {
    'name': f'{file_name}.jpg',
    'parents': ['1NUSd7suKgbbpLaTPIGhb1MdxLJqVKh7P']
    }
    media = MediaFileUpload(f'{file_name}',
                            mimetype='image/jpeg',
                            resumable=True)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print ('File ID: ' + file.get('id'))
    
uploadFile('horse.jpg')
#uploadFile()