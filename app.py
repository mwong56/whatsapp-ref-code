import platform

from flask import Flask, request
from twilio.rest import Client

account_sid = 'ACXXXXXXXXXXXXXXXXXXXXXXX'
auth_token = '[AuthToken]'
client = Client(account_sid, auth_token)
app = Flask(__name__)

# MESSAGES NEED TO BE HSM OR FROM/TO PAIR NEED TO BE IN 24 HOUR WINDOW
messages_to_send = ['Your Twilio code is 1238432',
                    'Your appointment is coming up on July 21 at 3PM',
                    'Your Yummy Cupcakes Company order of 1 dozen frosted cupcakes has shipped and should be delivered on July 10, 2019. Details: http://www.yummycupcakes.com/']
message_sids = []

print("sending first message")
message_sids.append(client.messages.create(
    body=messages_to_send.pop(0),
    from_='whatsapp:+14155238886',  # sandbox number
    to='whatsapp:+15101234567',
    status_callback='http://a22814a6.ngrok.io/callback').sid)


@app.route('/callback', methods=['POST'])
def callback():
    print("Received callback", request.form)
    message_status = request.form['MessageStatus']
    sid = request.form['MessageSid']

    # Check if callback we got back is related to the message we sent
    if sid != message_sids[-1]:
        return "ok"
    # Check we still have messages left to send
    if len(messages_to_send) == 0:
        return "ok"
    # Check message was delivered
    if message_status != 'delivered':
        return "ok"

    print("sending message")
    message_sids.append(client.messages.create(
        body=messages_to_send.pop(0),
        from_='whatsapp:+14155238886',  # sandbox number
        to='whatsapp:+15101234567',
        status_callback='http://a22814a6.ngrok.io/callback'
    ).sid)

    return "ok"


if __name__ == '__main__':
    # Check the System Type before to decide to bind
    # If the system is a Linux machine -:)
    if platform.system() == "Linux":
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
    # If the system is a windows /!\ Change  /!\ the   /!\ Port
    elif platform.system() == "Windows":
        app.run(host='0.0.0.0', port=50000, debug=True, use_reloader=False)
