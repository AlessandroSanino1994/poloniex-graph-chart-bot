import websocket
import json
import requests
import urllib
import os

# Suppress InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

###VARIABLES THAT YOU NEED TO SET MANUALLY IF NOT ON HEROKU#####
BOT_ID = os.environ['BOT-ID']
BOT_NAME = os.environ['BOT-NAME']
TOKEN = os.environ['SLACK-TOKEN']
###############################################################

def parse_join(message):
        """Parses a received message and does actions based on the type of the message."""
    #try:
        receivedMessage = json.loads(message)
        #print '\033[91m' + str(m) + '\033[0m'
        if (receivedMessage['type'] == 'channel_joined'):
                print '\033[91m I JOINED A CHANNEL \033[0m'
            #try:
                chan = receivedMessage['channel']['id']
                req = rtm_open_channel()
                params = {
                  'channel' : chan,
                  'token' : TOKEN,
                  'text' : 'Hello to everybody, looks like you need my help in this channel, what can I do for you?',
                  'parse' : 'full',
                  'as_user' : 'true'
                }
                resp = requests.post('https://slack.com/api/chat.postMessage', params=params)
            #except Exception as ex:
            #    print ex
        elif (receivedMessage['type'] == 'message') and receivedMessage['user'] != BOT_ID:
                print '\033[91m MESSAGE RECEIVED \033[0m'
            #try:
                receivedText = receivedMessage['text']
                chan = receivedMessage['channel']
                if '@' + BOT_ID in receivedText: #message for me
                    if 'help' in receivedText:
                        req = rtm_open_channel(channel=chan)
                        params = {
                          'channel' : chan,
                          'token' : TOKEN,
                          'text' : 'You can ask me any graph by using \n '+
                                   '`@' + BOT_NAME + ' graph [COIN1] [COIN2] [TIME]`\n'+
                                   'where `TIME` is 24h, 7d, 30d, 1y. \n' +
                                   'And of course sir. `COIN1` and `COIN2` are coins\n' +
                                   'Example of call may be `@' + BOT_NAME + ' graph ARK USD 24h`',
                          'parse' : 'full',
                          'as_user' : 'true'
                        }
                        resp = requests.post('https://slack.com/api/chat.postMessage', params=params)
                        print '\033[91m HELP MESSAGE POSTED \033[0m'
                    elif 'graph' in receivedText:
                        #try:
                            message_args = receivedText.split(' ')
                            params = {
                              'channel' : chan,
                              'token' : TOKEN,
                              'attachments' : None,
                              'parse' : 'full',
                              'as_user' : 'true'
                            }
                            coin1 = message_args[2].lower()
                            coin2 = message_args[3].lower()
                            timeframe = message_args[4].lower()

                            if not timeframe in ['24h', '7d', '30d', '1y']:
                                response_text = 'Invalid time frame sir. , the available options are : [24h, 7d, 30d, 1y]\n.'
                                response_text += 'Please ask me more by typing `@' + BOT_NAME + ' help`'
                            else: #tries to get image
                                #building url
                                url = 'https://cryptohistory.org/charts/candlestick/'
                                url += coin1 + '-' + coin2 + '/' + timeframe + '/png'
                                resp = requests.get(url)
                                if resp.status_code == requests.codes.ok:
                                    resp = requests.get('https://api.cryptonator.com/api/ticker/' + coin1 + '-' + coin2)
                                    if(resp.code == requests.codes.ok):
                                        resp = resp.json()
                                        response_text = '\nThe current price of ' + coin1.upper() + ' is ' + resp['ticker']['price'] + ' ' + coin2.upper() + /
                                        'with a current Volume of ' + resp['ticker']['volume'] + ' ' + coin2.upper()
                                    else:
                                        response_text = 'Current Price and Volume are not available, but I have the graph, sir.''
                                    title = coin1.upper() + ' - ' + coin2.upper() + ' '
                                    if (timeframe == '24h'):
                                        title += '24 Hours'
                                    elif (timeframe == '7d'):
                                        title += '7 Days'
                                    elif (timeframe == '30d'):
                                        title += '30 Days'
                                    elif (timeframe == '7d'):
                                        title += '1 Year'
                                    else:
                                        title += 'Invalid Timeframe [please contact my developer to fix this]'
                                    title += ' graph'
                                    params['attachments'] = json.dumps([
                                        {
                                            'pretext' : response_text,
                                            'fallback': 'Crypto Graph',
                                            'color': '#36a64f',
                                            'title': title,
                                            'image_url': url,
                                            'thumb_url': url
                                        }
                                    ])
                                    #print str(params)
                                else:
                                    response_text = 'Excuse me sir, but I can\'t find the coin pair you are asking for.\n'
                                    response_text += 'Please have in mind that I get data from Poloniex archives.'
                                    params['text'] = response_text
                                resp = requests.post('https://slack.com/api/chat.postMessage', params=params)
                        #except Exception as ex:
                            #print ex
                    elif 'thank you' in receivedText or 'thanks' in receivedText:
                        #try:
                            req = rtm_open_channel(channel=chan)
                            params = {
                              'channel' : chan,
                              'token' : TOKEN,
                              'text' : 'You\'re welcome sir. It\'s a pleasure to me to be helpful. :)',
                              'parse' : 'full',
                              'as_user' : 'true'
                            }
                            resp = requests.post('https://slack.com/api/chat.postMessage', params=params)
                            print '\033[91m YOU\'RE WELCOME MESSAGE POSTED \033[0m'
                        #except Exception as ex:
                        #    print ex
                    else:
                        #try:
                            req = rtm_open_channel(channel=chan)
                            params = {
                              'channel' : chan,
                              'token' : TOKEN,
                              'text' : 'Excuse me sir., but I don\'t understand what you are saying. May you ask me for help?\n `@' + BOT_NAME + ' help`',
                              'parse' : 'full',
                              'as_user' : 'true'
                            }
                            resp = requests.post('https://slack.com/api/chat.postMessage', params=params)
                            print '\033[91m I DON\'T UNDERSTAND MESSAGE POSTED \033[0m'
                        #except Exception as ex:
                        #    print ex
            #except Exception as ex:
            #    print ex
        elif(receivedMessage['type'] == 'hello'):
            print '\033[91m HELLO RECEIVED \033[0m'
        else: pass
    #except Exception as ex:
    #    print '\033[91m Exception : Message => ' + str(receivedMessage) + '\n Error :' + ex + ' \033[0m'

def start_rtm():
    """Connects to Slacks and initiates socket handshake, returns a websocket"""
    req = requests.get('https://slack.com/api/rtm.start?token='+TOKEN, verify=False)
    req = req.json()
    websocket_url = req['url']
    return websocket_url

def rtm_open_channel(channel):
    """Connects to Slacks and opens specified channel"""
    params = {
       'token' : TOKEN,
       'channel' : channel,
    }
    req = requests.get('https://slack.com/api/im.open', params=params)
    req = req.json()
    return req

def on_message(ws, message):
    parse_join(message)

def on_error(ws, error):
    print 'SOME ERROR HAS HAPPENED', error

def on_close(ws):
    print '\033[91m'+'Connection Closed'+'\033[0m'

def on_open(ws):
    print 'Connection Started'

if __name__ == '__main__':
    r = start_rtm()
    ws = websocket.WebSocketApp(r, on_message = on_message, on_error = on_error, on_close = on_close)
    #ws.on_open
    ws.run_forever()
