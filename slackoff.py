import os, json,time,feedparser, pyowm
import time
from slackclient import SlackClient
# MAKE SURE TO NOT UPLOAD THE FREAKING TOKEN IN THE FUTURE.
# Currently hardcoded to specific user IDs. This doesnt generalize to other teams well. Need to fix this in the interest of open source.
BOT_ID = os.environ.get("BOT_ID")
GENERAL_ID = os.environ.get("GENERAL_ID")
DB_ID = os.environ.get("DBID")
DM_ID = os.environ.get("DMID")
PM_ID = os.environ.get("PMID")
BM_ID = os.environ.get("BMID")
WEATHER_KEY = os.environ.get("PY_OWM_API")

owm = pyowm.OWM(WEATHER_KEY)  

# This is handled poorly. Will need changing if I am ever hosting this long term (raspberry pi idea).
now = time.strftime("%c")
accessDict = {DB_ID : now,DM_ID:now,PM_ID:now,BM_ID:now}
#print accessDict
# constants
AT_BOT = "<@" + BOT_ID + ">"

self_deprecation = 'self deprecation'

find_last = 'last access'


# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


#def handle_command(command):
#    """
#        Receives commands directed at the bot and determines if they
#        are valid commands. If so, then acts on the commands. If not,
#        returns back what it needs for clarification.
#    """
#    api_call = slack_client.api_call("users.list")
#    users = api_call.get('members')

 #   if command[0].startswith(self_deprecation) or command[0].startswith(self_dep2) :
 #   	response = "<@"+command[2]+"> --"
 #       slack_client.api_call("chat.postMessage", channel=command[1],
 #                             text=response,link_names=True, as_user=True)
 #   elif command[0].startswith(gtfo):
 #   	response = ""
 #       slack_client.api_call("chat.postMessage", channel=command[1],
 #           text=response,link_names=True, as_user=True)
 #   elif command[0].startswith(find_last):
 #   	access = slack_client.api_call("team.accessLogs")
 #   	print access



def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    
    if output_list and len(output_list) > 0:
        for output in output_list:
            if 'user' in output:
                user = slack_client.api_call('users.info',user=output['user'])
            print output['type']
            
            if output['type'] == 'message' and  'text' in  output and AT_BOT in output['text']:
                print output['text']
                if 'weather' in output['text'].lower():
                    ix = output['text'].index(':')
                    place = output['text'][ix+1:] 
                    obs = owm.weather_at_place(place)
                    weather = obs.get_weather()
                    status = weather.get_status() 
                    temp = str(weather.get_temperature('fahrenheit')['temp'])
                    message= "In " + place + ' it is ' + temp + ' degrees and ' + status
                    slack_client.api_call("chat.postMessage",channel=GENERAL_ID,text=message,link_names=True, as_user=True)
    


                if 'latest gb' in output['text'].lower():
                    if 'vid' in output['text'].lower():
                        gb =  feedparser.parse('http://www.giantbomb.com/feeds/video/.rss/')
                        message= "#Content #Monetize " + gb.entries[0]['link']
                        slack_client.api_call("chat.postMessage",channel=GENERAL_ID,text=message,link_names=True, as_user=True)
                    #print gb.entries[0]['link'] 
                    elif 'podcast' in output['text'].lower():
                        gb =  feedparser.parse('http://www.giantbomb.com/feeds/podcast/.rss/')
                        message= "#Content #Monetize " + gb.entries[0]['link']
                        slack_client.api_call("chat.postMessage",channel=GENERAL_ID,text=message,link_names=True, as_user=True)                     

                if 'reddit top' in output['text'].lower():
                    print output['text']
                    ix = output['text'].index(':')
                    sub = output['text'][ix+1:]
                    link = 'https://www.reddit.com/r/'+sub+'.rss'
                    reddit = feedparser.parse(link)
                    message= "Top Post from " + sub + ' ' + reddit.entries[0]['link']
                    slack_client.api_call("chat.postMessage",channel=GENERAL_ID,text=message,link_names=True, as_user=True)


                if 'last online' in output['text']:
                    global accessDict
                    usr = output['user']
                    #user = slack_client.api_call('users.info',user=output['user'])
                    message = 'Hey  '  + user['user']['profile']['first_name'] + '.You were last online: ' + accessDict[usr] + '. You can enter this timestamp into the search function with before:"your timestamp" to view messages around this time!'
                    dmInfo = slack_client.api_call('im.open',user=output['user'])
                    slack_client.api_call("chat.postMessage",channel=dmInfo['channel']['id'],text=message,link_names=True, as_user=True)
                    #print dmInfo['channel']['id']
                    #print output['text']



            if output['type'] == 'presence_change' and output['presence'] == 'active':
                channels = slack_client.api_call('channels.list')
                #print slack_client.api_call('channels.list')
                if 'bot_id' not in user['user']['profile']:
                    message = 'Welcome Back ' + user['user']['profile']['first_name'] + '. To view messages since you were last on enter command @slackoff last online'
                    slack_client.api_call("chat.postMessage",channel=GENERAL_ID,text=message,link_names=True, as_user=True)

            if output['type'] == 'presence_change' and output['presence'] == 'away' and 'bot_id' not in user['user']['profile']:
                if output['user'] == DB_ID:
                    DB_LAST = int(time.time())
                    accessDict = {DB_ID : DB_LAST}
                elif output['user'] == DM_ID:
                    DM_LAST  = int(time.time())
                    accessDict[DM_LAST] = DM_LAST
                elif output['user'] == PM_ID:
                    PM_LAST = int(time.time())
                    accessDict[PM_LAST] = PM_LAST
                elif output['user'] == BM_ID:    
                    BM_LAST = int(time.time())
                    accessDict[BM_LAST] = BM_LAST


            #if output and 'text' in output and AT_BOT in output['text'] and 'user' in output and 'channel' in output:
            #    # return text after the @ mention, whitespace removed
            #    command = output['text'].split(AT_BOT)[1].strip().lower()
            #    channel = output['channel']
            #    user = output['user']

                return command, channel, user
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("SlackOff connected and running")
        #users = slack_client.api_call('users.list')
        #print(json.dumps(users, indent=4))

        while True:
            
            parse_slack_output(slack_client.rtm_read())
            #if command[0] and command[1] and command[2]:
                #handle_command(command)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")





