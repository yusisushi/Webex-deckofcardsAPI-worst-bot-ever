##################################################################
#     Libraries
##################################################################
import json
import random
import requests
import time

##################################################################
#     some variables
##################################################################
#webex vars
accessToken = "Bearer MTA4YzU4MzQtNTBjNS00YzM0LTkyZDAtNjIxNzU4NjAwZmQwZjhhNTJmOWEtZTQw_PF84_consumer"
chatroom_yuska = "Y2lzY29zcGFyazovL3VzL1JPT00vMDM2MWQyYzAtMGEwYy0xMWViLWFjMTEtZTUzMzQ3OGQwY2Y2"

#card vars
current_card_img =""
all_cards_img = ""
current_card = ""
cards_tot_int = int(0)
cards_tot_str = ""
choice = "choice_not_yet_defined"
deckname = "deckname_not_yet_defined"
file_var = ""
sendmessage_var = "sendmessage_var_not_yet_defined"


##################################################################
#     some useful functions
##################################################################
#restart script
def restart():
    import sys
    print("argv was",sys.argv)
    print("sys.executable was", sys.executable)
    print("restart now")

    import os
    os.execv(sys.executable, ['python'] + sys.argv)

#send message
def send_message():
    responseMessage = sendmessage_var
    HTTPHeaders = {
                        "Authorization": accessToken,
                        "Content-Type": "application/json"
                    }
    PostData = {
                        "roomId": chatroom_yuska,
                        "text": responseMessage,
                    }
    r = requests.post( "https://api.ciscospark.com/v1/messages",
                        data = json.dumps(PostData),
                        headers = HTTPHeaders,
                    )
    print("Sending to Webex Teams: ", sendmessage_var)

def send_w_image():
    responseMessage = sendmessage_var
    HTTPHeaders = {
                        "Authorization": accessToken,
                        "Content-Type": "application/json"
                    }
    PostData = {
                        "roomId": chatroom_yuska,
                        "text":responseMessage,
                        "files": file_var
                    }
    r = requests.post( "https://api.ciscospark.com/v1/messages",
                        data = json.dumps(PostData),
                        headers = HTTPHeaders,
                    )
    print("Sending this image to Webex Teams: ", sendmessage_var)

#new deck
def new_deck():
    url = "https://deckofcardsapi.com/api/deck/new/"

    response = requests.get(url)
    json_data = json.loads(response.text)

    deckname = json_data["deck_id"]
    return(deckname)


#################################################################
#     Bot Step1, waits to be called by "/21"
#################################################################
while True:
    #1 second of delay to the loop to not go over a rate limit of API calls
    time.sleep(1)
    GetParameters = {
                            "roomId": chatroom_yuska,
                            "max": 1
                        }
    # run the call against the messages endpoint of the Webex Teams API using the HTTP GET method
    r = requests.get("https://webexapis.com/v1/messages",
                        params = GetParameters,
                        headers = {"Authorization": accessToken}
                    )

    json_data = r.json()
    # store in array or something
    messages = json_data["items"]
    message = messages[0]["text"]
    print("Latest message: " + message)

    if message.find("/21") == 0:
        sendmessage_var = ("Thoust has called for me! Wishes thee to play a game...?")
        send_message()

        sendmessage_var = ("type '/yes' to begin or '/no' to cancel. ")
        send_message()
        break


#################################################################
#     Bot Step2, listens for "/yes" or "/no" to start the game
#################################################################
while True:
    #1 second of delay to the loop to not go over a rate limit of API calls
    time.sleep(1)

    GetParameters = {
                            "roomId": chatroom_yuska,
                            "max": 1
                        }
    # run the call against the messages endpoint of the Webex Teams API using the HTTP GET method
    r = requests.get("https://webexapis.com/v1/messages",
                        params = GetParameters,
                        headers = {"Authorization": accessToken}
                    )

    # listen to, and show last message
    json_data = r.json()
    # store in array or something
    messages = json_data["items"]
    message = messages[0]["text"]
    print("Latest message: " + message)

    # check if the text of the message starts with the magic character
    if message.find("/yes") == 0:
        sendmessage_var = "Another mortal wishes to take the challenge... Let's begin!"
        send_message()
        break

    elif message.find("/no") == 0:
        sendmessage_var = "That's okay... Maybe next time!"
        send_message()
        restart()


#################################################################
#     CARDS BOT
#################################################################

#################################################################
#     Draws first card
#################################################################
deckname = new_deck()
#sendmessage_var = ("Current deck_id is: "+deckname)
#send_message()

#shuffle carddeck
url = "https://deckofcardsapi.com/api/deck/" + deckname + "/shuffle/"
response = requests.get(url)
sendmessage_var = ("Shuffling deck with id: " +deckname)
send_message()

#draw first
url = "https://deckofcardsapi.com/api/deck/" + deckname + "/draw/?count=1"
response = requests.get(url)
json_data = json.loads(response.text)

sendmessage_var = ("Drawing first card...")
send_message()

current_card = json_data["cards"][0]['value']
if current_card == 'ACE':current_card = int(1)
if current_card == '1':current_card = int(1)
if current_card == '2':current_card = int(2)
if current_card == '3':current_card = int(3)
if current_card == '4':current_card = str(4)
if current_card == '5':current_card = int(5)
if current_card == '6':current_card = int(6)
if current_card == '7':current_card = int(7)
if current_card == '8':current_card = int(8)
if current_card == '9':current_card = int(9)
if current_card == '0':current_card = int(10)
if current_card == '10':current_card = int(10)
if current_card == 'JACK':current_card = int(11)
if current_card == 'QUEEN':current_card = int(12)
if current_card == 'KING':current_card = int(13)
cards_tot_int = int(cards_tot_int) + int(current_card)
print (cards_tot_int)
#convert integer to string for sending message
cards_tot_str = str(cards_tot_int)
print ("cards tot string:", cards_tot_str)

sendmessage_var = ("Your card is: the " +json_data["cards"][0]['value'] +" of " +json_data["cards"][0]['suit'] +", "+ "and your total value is: " +cards_tot_str)
file_var = (json_data["cards"][0]['images']['png'])
send_w_image()

remaining_str = (str)(json_data["remaining"])
if remaining_str != '1':
    sendmessage_var = ("There are " +remaining_str +" cards remaining.")
else:
    sendmessage_var = ("There is only 1 card remaining.")
send_message()

#################################################################
#     Second card yes/no?
#################################################################
sendmessage_var = ("Draw another card? (type '/yes' or '/no') ")
send_message()

#################################################################
#     Another card yes/no?
#################################################################
while True:
    #1 second of delay to the loop to not go over a rate limit of API calls
    time.sleep(1)

    GetParameters = {
                            "roomId": chatroom_yuska,
                            "max": 1
                        }
    # run the call against the messages endpoint of the Webex Teams API using the HTTP GET method
    r = requests.get("https://webexapis.com/v1/messages",
                        params = GetParameters,
                        headers = {"Authorization": accessToken}
                    )

    # listen to, and show last message
    json_data = r.json()
    # store in array or something
    messages = json_data["items"]
    message = messages[0]["text"]
    print("Latest message: " + message)

    # check if the text of the message starts with the magic character
    if message.find("/yes") == 0:
        sendmessage_var = ("Okay, drawing 1 more card.")
        send_message()

        url = "https://deckofcardsapi.com/api/deck/" + deckname + "/draw/?count=1"
        response = requests.get(url)
        json_data = json.loads(response.text)

        current_card = json_data["cards"][0]['value']
        if current_card == 'ACE':current_card = int(1)
        if current_card == '1':current_card = int(1)
        if current_card == '2':current_card = int(2)
        if current_card == '3':current_card = int(3)
        if current_card == '4':current_card = int(4)
        if current_card == '5':current_card = int(5)
        if current_card == '6':current_card = int(6)
        if current_card == '7':current_card = int(7)
        if current_card == '8':current_card = int(8)
        if current_card == '9':current_card = int(9)
        if current_card == '0':current_card = int(10)
        if current_card == '10':current_card = int(10)
        if current_card == 'JACK':current_card = int(11)
        if current_card == 'QUEEN':current_card = int(12)
        if current_card == 'KING':current_card = int(13)
        cards_tot_int = cards_tot_int + current_card
        cards_tot_str = str(cards_tot_int)

        sendmessage_var = ("Your new card is: the " +json_data["cards"][0]['value'] +" of " +json_data["cards"][0]['suit'] +", "+ "and your total value is: " +cards_tot_str)
        file_var = (json_data["cards"][0]['images']['png'])
        send_w_image()

        cards_tot_str = str(cards_tot_int)
        if cards_tot_int == 21:
            sendmessage_var = ("Holy POOPSIEDDAISY! Your total is: " +cards_tot_str +"!")
            send_message()
            restart()
        elif cards_tot_int >= 22:
            sendmessage_var = ("Your new total value is: " +cards_tot_str)
            send_message()
            sendmessage_var = ("THEE has past the value of 21. You loose your dignity and your soul is now MINE!")
            send_message()
            restart()
        else:
            sendmessage_var = ("Your new total value is: " +cards_tot_str)
            send_message()

        remaining_str = (str)(json_data["remaining"])
        if remaining_str != '1':
            sendmessage_var = ("There are " +remaining_str +" cards remaining.")
        else:
            sendmessage_var = ("There is only 1 card remaining.")
        send_message()

        sendmessage_var = ("Draw another card? (type '/yes' or '/no') ")
        send_message()

        sendmessage_var = ("There are", json_data["remaining"],"cards remaining.")
        send_message()

    elif message.find("/no") == 0:

        sendmessage_var = ("Your total is " +cards_tot_str)
        send_message()

        if remaining_str != '1':
            sendmessage_var = ("There are " +remaining_str +" cards remaining.")
        else:
            sendmessage_var = ("There is only 1 card remaining.")
        send_message()
        restart()
