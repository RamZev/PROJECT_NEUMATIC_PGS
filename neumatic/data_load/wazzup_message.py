import requests
import json

url = "https://api.wazzup24.com/v3/message"

payload = json.dumps({
  "channelId": "4e91acb6-fbeb-41c1-93f9-661b1f8c088e",
  "chatId": "51983981484",
  "chatType": "whatsapp",
  "contentUri": "https://www.dropbox.com/scl/fi/dspaec5pu2o6bmtv0f29q/NEURAL-DEVS_AZUL.png?rlkey=bng3xiw1fvhapeemwu8fkrppy&st=i3uqn3hl&dl=0"
})
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer a309438bd67d4489bc277f0a756310d0'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
