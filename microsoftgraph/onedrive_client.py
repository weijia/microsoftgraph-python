import os

import requests

from microsoftgraph.client import Client
from microsoftgraph.decorators import token_required


class OneDriveClient(Client):
    @token_required
    def upload_file(self, folder_id, file_path):
        filename = os.path.basename(file_path)
        url = "https://graph.microsoft.com/beta//me/drive/items/{folder_id}:/{filename}:/content".format(**{
            "folder_id": folder_id,
            "filename": filename,
        })
        with open(file_path, "rb") as f:
            _headers = {
                'Accept': 'application/json',
            }
            if self.office365:
                _headers['Authorization'] = 'Bearer ' + self.office365_token['access_token']
            else:
                _headers['Authorization'] = 'Bearer ' + self.token['access_token']
            method = "PUT"
            _headers.update({'Content-type': 'application/octet-stream'})
            data = f.read()
            _headers.update({'Content-Length': str(len(data))})
            return self._parse(requests.request(method, url, headers=_headers, data=data))
