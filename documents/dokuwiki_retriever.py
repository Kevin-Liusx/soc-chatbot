import requests
import json

DOKUWIKI_URL = "https://dochub-dev.comp.nus.edu.sg/lib/exe/jsonrpc.php"

USERNAME = "e1053635"
PASSWORD = "keVin2003413?"


payload = {
    "jsonrpc": "2.0",
    "method": "core.getWikiVersion",
    USERNAME: "e1053635",
    PASSWORD: "keVin2003413?",
    "id": 1
}

headers = { "Content-Type": "application/json" }

response = requests.post(DOKUWIKI_URL, data=json.dumps(payload), headers=headers, auth=(USERNAME, PASSWORD))

if response.status_code == 200:
    print(response.json())
else:
    print("Error:", response.status_code, response.text)