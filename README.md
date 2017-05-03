# SlackOff
The goal of SlackOff is to have an ever increasing number of useful Slack tools. These tools will be available by calling SlackOff's chat bot with commands associated with certain tools. The first tool in development is a simple navigation tool which allows a user to revert the chat back to the moment they were last online. This allows the user to read any and all messages they may have missed. As tools are finished this readme will be editted to show finished tools, in progress tools, and planned tools.

# In Progress
ImportantList: Allow users to create lists of things they want other users to take note of
# Finished
LastTimeActive: call command '@slackoff last online'. Bot returns time stamp user was last online, searchable in messages with 'before:returnedTimeStamp'. Unfortunately bots are unable to do the search.messages API.

LatestGBVid: call command '@slackoff latest gb vid'. Sends message with latest GiantBomb.com video content.

LatestGBPod: call command '@slackoff latest gb pod'. Sends message with latest GiantBomb.com podcast.
NOTE: *Probably* done. Need to properly test when I get a new slack token

LocalForecast: call command '@slackoff weather:city,State. Returns a message with the temperature and conditions of given city state. Works nationally too with city,country. State and country are two letter abbreviations i.e Boulder,CO, London,GB.

RedditTop: call command '@slackoff top reddit:'subName'. Returns link to top post of given subreddit
