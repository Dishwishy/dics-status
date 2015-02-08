import requests
import json

#constants
#facebook group URL
fbURL = "https://graph.facebook.com/384776165021681/feed"

#import API keys
f = open("/home/kyle/DICS_status/APIkeys.json")
keyData = json.loads(f.read())
f.close()
xbKey = keyData['xbapikey']
fbKey = keyData['fbapikey']
xbHeaders = {'X-AUTH' : xbKey }
fbAuthForm = {'access_token' : fbKey }

#user IDs for XBOX
boneList = \
{ 'kyle'  : '2533274809127358',
'colburn' : '2535449548043467',
'ed' : '2533274821230520',
'phil' : '2533274879435275',
#ryansul : '275912495028211',
'gorka' : '2533274816880090',
'daniel' : '2533274813492825'}



#method to generate URL
def xbapiURL(xuid):
    url = "https://xboxapi.com/v2/" + xuid + "/presence"
    return url

def xbPresenseParse(gamerTagList):
    message = "A Friendly Reminder from Robo-DIC: \n"
    for name, xid in gamerTagList.iteritems():
        xbAPIreq = requests.get(xbapiURL(xid), headers=xbHeaders)
        presMsg = json.loads(xbAPIreq.text)
        if 'error_message' in presMsg:
            print "Error from XBOX API: " + str(presMsg["error_code"])
            return 0
        print presMsg
        if (presMsg['state'] != "Offline"):
           try:
               message = message + name + " is currently playing " + presMsg["devices"][0]["titles"][1]["name"]+ "\n"
           except:
               print presMsg
           else:
               message = message + name + " is currently playing " + presMsg["devices"][0]["titles"][0]["name"] + "\n"
        else:
           message = message + name + " is offline \n"
    return message


#get our message from xbox API
xbMessage = xbPresenseParse(boneList)
if xbMessage == 0:
    print "Error calling xbox API, no data posted to facebook"
else :
    #add new key value pair to dictionary
    fbAuthForm['message'] = xbMessage
    fbAPIreq = requests.post(fbURL, data = fbAuthForm )
    fbResponse =  json.loads(fbAPIreq.text)
    if 'error' in fbResponse:
        print "Error with Facebook API " + fbResponse["error"]["type"]
        print fbResponse
    else :
        print fbResponse







