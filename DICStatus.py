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
#you'll have to use the xboxapi to get these
#or scrape them from your login
boneList = \
{ 'kyle'  : '2533274809127358',
'colburn' : '2535449548043467',
'ed' : '2730307274094389',
'phil' : '2533274879435275',
'gorka' : '2533274816880090',
'daniel' : '2533274813492825'}



#method to generate URL
def xbapiURL(xuid):
    url = "https://xboxapi.com/v2/" + xuid + "/presence"
    return url

def xbPresenseParse(gamerTagList):
    destinyCtr = 0
    gamerListLen = len(boneList)
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
               curPlay = presMsg["devices"][0]["titles"][1]["name"]
           except:
               curPlay = presMsg["devices"][0]["titles"][0]["name"] 
           if curPlay == "Destiny":
               destinyCtr += 1
           message = message + name + " is currently playing " + curPlay + "\n" 
        else:
           message = message + name + " is offline \n"
    if destinyCtr >= 3:
        return message
    else:
        return 0


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







