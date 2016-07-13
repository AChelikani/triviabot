import os
import time
from slackclient import SlackClient
import config # Importing API keys and Bot ID
import urllib, json

BOT_ID = config.TRIVIA_BOT_ID

AT_BOT = "<@" + BOT_ID + ">:"
COMMANDS = ["ask"]
TRIVIA_URL = ""

slack_client = SlackClient(config.SLACK_API_KEY)

def handle_invalid():
    return "Invalid Command! Type help to see all commands."

def handle_ask(value):
    try:
        value = int(value)
        if (value >= 100 and value <= 1000 and value%100 == 0):
            url = TRIVIA_URL + str(value)
            response = urllib.urlopen(url)
            data = json.loads(response.read())
            print len(data)
            return "good question"
        else:
            return "Invalid difficulty!"
    except:
        return "Invalid difficulty, not a number!"

def parse_command(command):
    args = command.split(" ")
    if len(args) > 0:
        if args[0] == "ask":
            try:
                value = args[1]
                return handle_ask(value)
            except:
                return handle_invalid()
    return handle_invalid()


def handle_command(command, channel):
    response = parse_command(command)
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                print output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if slack_client.rtm_connect():
        print "Triviabot connected and running!"
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
