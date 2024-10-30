##########################################################
# Apple Newsroom Notification Server
# (c)pschuelpen
#
# www.pschuelpen.com/
#
# Notifications for new Apple News
#
# Optimized for:
# Python3 - Running on any computer
#
##########################################################
# Import Libraries
##########################################################


import os
import requests
import feedparser
import time
import yaml
import json
from openai import OpenAI


#####################################
#            Functions 
#####################################

####
# Format the message

def formatMessage(entry):

    message = "Title: " + entry.title + " | Summary: " + entry.summary + " | Content " + entry.content + " | Priorities: " + PRIORITIES

    return message

####
# Send message to the ntfy.sh server

def sendMessage(title, message):
   
    headers = {
            'Title': f"RaspberryPi News - {title}",
            'Priority': NTFY_PRIORITY,
            'Tags': "strawberry"
    }
    
    try:
        req = requests.post(url=NTFY_BASE_URL + '/' + NTFY_TOPIC, data=message, headers=headers, timeout=20)
    except requests.exceptions.Timeout:
        print('Request Timeout')
        pass
    except requests.exceptions.TooManyRedirects:
        print('Too many requests')
        pass
    except requests.exceptions.RequestException as e:
        print(e)
        pass

####
# Load credentials from the yaml file

def load_credentials(filepath):
    try:
        with open(filepath, 'r') as file:
            credentials = yaml.safe_load(file)
            ntfy_topic = credentials['ntfy-topic']
            openai_key = credentials['openai-api-key']
            priorities = credentials['topic-priorities']
            return ntfy_topic, openai_key, priorities
    except Exception as e:
        print("Failed to load credentials: {}".format(e))
        raise


def create_ai_summary(message):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """
                You have to summarize this message in a small format such that this message can be sent as a notification. 
                Keep it short and categorize if it is relevant to me based on my Priorities. Please always answer in a json formal string. 
                Meaning you have to return a json object with the key 'type_match', 'short_title' and 'summary' where type will be true or false, short_title a very short title for the notification and summary will be the summarized message.
                """
            },
            {"role": "user", "content": message}
        ],
        model="gpt-4"
    )

    # Convert response to JSON
    response_content = response.choices[0].message.content

    try:
        data = json.loads(response_content)
    except json.JSONDecodeError:
        print(response_content)
        print("Response content is not a valid JSON format")
        exit()

    return bool(data['type_match']), data["short_title"], data['summary']



#####################################
#              Setup 
#####################################

# Load credentials
NTFY_TOPIC, OPENAI_API_KEY, PRIORITIES = load_credentials('./config.yaml')

client = OpenAI(
    # This is the default and can be omitted
    api_key=OPENAI_API_KEY
)


# Feed URL - Apple Newsroom
FEED_URL = 'https://www.raspberrypi.com/news/feed/'

# settings for ntfy
NTFY_BASE_URL = 'https://ntfy.sh'
NTFY_PRIORITY = 'default'

# User Agent
USER_AGENT = 'Apple News'

# Waiting Interval in Minutes
WAITING_INTERVAL = 1


#####################################
#              Main 
#####################################


# Set control to blank list
control = []

# Fetch the feed
f = feedparser.parse(FEED_URL, agent=USER_AGENT)

# If there are entries in the feed, add entry guid to the control variable
if f.entries:
    for entries in f.entries:
        control.append(entries.id)

#Only wait 30 seconds after initial run.
time.sleep(30)


while True:
    # Fetch the feed again, and again, and again...
    f = feedparser.parse(FEED_URL, agent=USER_AGENT)

    # Compare feed entries to control list.
    # If there are new entries, send a message/push
    # and add the new entry to control variable
    for entries in f.entries:
        if entries.id not in control:

            # Format the message
            message = formatMessage(entries)

            # Get ChatGPT Summary and priorization
            not_bool, title, summary = create_ai_summary(message)

            # Only if that new message is relevant to user send a notification
            if not_bool:
                sendMessage(title, summary)

            # Add entry guid to the control variable
            control.append(entries.id)

    time.sleep((WAITING_INTERVAL * 60) - 1)
