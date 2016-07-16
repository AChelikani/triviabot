import os
import time
from slackclient import SlackClient
import config # Importing API keys and Bot ID
import random
from trivia_questions import *

BOT_ID = config.TRIVIA_BOT_ID

AT_BOT = "<@" + BOT_ID + ">:"
COMMANDS = {
    "ask random"   : "Triviabot will ask you a random trivia question.",
    "leaderboard"  : "Triviabot will display the current leaderboard.",
    "help"         : "Triviabot will list out all the commands"
}
TRIVIA_URL = ""
NUM_TRIVIA_QUESTIONS = len(TRIVIA_QUESTIONS)
current_answer = ""
question_in_progress = False
leaderboard = {}

slack_client = SlackClient(config.SLACK_API_KEY)

def parse_command(command, user):
    global current_answer
    global question_in_progress
    clist = command.split(" ")
    if (not question_in_progress):
        if (clist[0] == "ask"):
            if (len(clist) > 1):
                if (clist[1] == "random"):
                    question, current_answer = get_random_question(NUM_TRIVIA_QUESTIONS)
                    question_in_progress = True
                    return format_string(question)
                else:
                    return "Invalid use of ask!"
            else:
                return "Invalid Command!"
        elif (command == "leaderboard"):
            return display_leaderboard()
        elif (command == "help"):
            return display_help()
        else:
            return "Invalid Command!"
    else:
        if (command == current_answer):
            current_answer = ""
            question_in_progress = False
            update_leaderboard(user, 1)
            return "Correct answer " + format_string(get_username(user))
        else:
            return "Incorrect"

def display_help():
    res = ""
    for command in COMMANDS:
        res += format_string(command) + ": " + format_string(COMMANDS[command]) + "\n"
    return res

def update_leaderboard(user, change):
    global leaderboard
    user = get_username(user)
    if user in leaderboard:
        leaderboard[user] += change
    else:
        leaderboard[user] = change
    print leaderboard

def display_leaderboard():
    res = ""
    for user in leaderboard:
        res += format_string(user + ": " + str(leaderboard[user])) + "\n"
    return res

def get_random_question(size):
    c = random.randint(1,size)
    question = TRIVIA_QUESTIONS[c]["question"]
    answer = TRIVIA_QUESTIONS[c]["answer"]
    return question, answer

def format_string(s):
    return "`" + s + "`"


def handle_command(command, channel, user):
    response = parse_command(command, user)
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def get_username(user):
    return slack_client.api_call("users.info", user=user)['user']['name']

def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel'], \
                       output['user']
    return None, None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if slack_client.rtm_connect():
        print "Triviabot connected and running!"
        while True:
            command, channel, user = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel, user)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
