import requests
import json

URL = 'https://www.sms4india.com/api/v1/sendCampaign'

# get request
def sendPostRequest(reqUrl, apiKey, secretKey, useType, phoneNo, senderId, textMessage):
  req_params = {
  'apikey':"VXYJ7QJWKH4LQDEQLF91NTTQQXDTA2VK",
  'secret':"DJ7PCPJJKTKAHMRF",
  'usetype':"stage",
  'phone': 6300040845,
  'message':textMessage,
  'senderid':8742855607
  }
  return requests.post(reqUrl, req_params)


# response = sendPostRequest(URL, 'provided-api-key', 'provided-secret', 'prod/stage', 'valid-to-mobile', 'active-sender-id', 'message-text' )


# print (response.text)