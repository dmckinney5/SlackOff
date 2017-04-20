import os, json
import time
from slackclient import SlackClient

BOT_ID = os.environ.get("BOT_ID")
GENERAL_ID = 'C1Q371LJ3'
# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"
self_deprecation = 'self deprecation'
self_dep2 = 'just fuck my shit up'
find_last = 'last access'
gtfo = 'just fuck off'
pin = 'pin'

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def handle_command(command):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    api_call = slack_client.api_call("users.list")
    users = api_call.get('members')

    if command[0].startswith(self_deprecation) or command[0].startswith(self_dep2) :
    	response = "<@"+command[2]+"> --"
        slack_client.api_call("chat.postMessage", channel=command[1],
                              text=response,link_names=True, as_user=True)
    elif command[0].startswith(gtfo):
    	response = ""
        slack_client.api_call("chat.postMessage", channel=command[1],
            text=response,link_names=True, as_user=True)
    elif command[0].startswith(find_last):
    	access = slack_client.api_call("team.accessLogs")
    	print access



def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    #print output_list
    if output_list and len(output_list) > 0:
        for output in output_list:
            #print output['type']
            if output['type'] == 'presence_change' and output['presence'] == 'active':
                #UID = output['user']
                user = slack_client.api_call('users.info',user=output['user'])
                #print user['real_name']

                channels = slack_client.api_call('channels.list')
                print(json.dumps(channels, indent=4))

                #print user['user']['profile']['real_name']
                #print slack_client.api_call('channels.list')
                if 'bot_id' not in user['user']['profile']:
                    message = 'Welcome Back ' + user['user']['profile']['first_name']
                    slack_client.api_call("chat.postMessage",channel=GENERAL_ID,text=message,link_names=True, as_user=True)
                #if 

                #user = slack_client.api_call('users.info',output['user'])
                #print user['real_name']

            if output and 'text' in output and AT_BOT in output['text'] and 'user' in output and 'channel' in output:
                # return text after the @ mention, whitespace removed
                command = output['text'].split(AT_BOT)[1].strip().lower()
                channel = output['channel']
                user = output['user']

                return command, channel, user
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("SlackOff connected and running")
        users = slack_client.api_call('users.list')
        print(json.dumps(users, indent=4))

        while True:
            #slack_client.rtm_read()
            parse_slack_output(slack_client.rtm_read())
            #if command[0] and command[1] and command[2]:
            #    handle_command(command)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")





