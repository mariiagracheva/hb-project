import random
import base64
import hashlib
import json
import requests
import os
from datetime import datetime

nonce = hashlib.sha1().hexdigest()
created = datetime.now().strftime("%Y-%m-%dT%H:%M:%S-0800")

Username="mariiagracheva"
Key=VOLUNTEERMATCH_API_KEY
PasswordDigest = base64.b64encode(hashlib.sha256((nonce+created+Key).encode('utf-8')).digest())
url = "https://www.volunteermatch.org/api/call"
 
query_params = {}
action_param = "getKeyStatus"

params = {"action": action_param, "query": json.dumps(query_params)}

custom_headers = {
    "Authorization": 'WSSE profile="UsernameToken"',
    "X-WSSE": u'UsernameToken Username="{}", \
            PasswordDigest="{}", \
            Nonce="{}", \
            Created="{}"'.format(Username, PasswordDigest, nonce, created)
}


keyStatus = requests.get(url, params=params, headers=custom_headers)