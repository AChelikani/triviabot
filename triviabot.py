import os
import time
from slackclient import SlackClient
import config # Importing API keys and Bot ID
import random
import json
# import sqlite3

# TODO: Implement drawing questions from a database

NUM_TRIVIA_QUESTIONS = 0
trivia_question_list = []

# Currently JSON should be in the form of a list of JSONS with
# at least: question, answer, category, and value keys

with open("jeopardy.json") as json_file:
    json_data = json.load(json_file)
    NUM_TRIVIA_QUESTIONS = len(json_data)
    trivia_question_list = json_data

BOT_ID = config.TRIVIA_BOT_ID

AT_BOT = "<@" + BOT_ID + ">:"
COMMANDS = {
    "ask random"   : "Triviabot will ask you a random trivia question.",
    "leaderboard"  : "Triviabot will display the current leaderboard.",
    "help"         : "Triviabot will list out all the commands.",
    "skip"         : "Triviabot will skip the current question."
}

# Global vars
current_answer = ""
current_point_value = 0
question_in_progress = False
leaderboard = {}

# Configure the slack client with API key
slack_client = SlackClient(config.SLACK_API_KEY)

# Parses a command to figure out appropriate way of dealing with the command
# All commands must be in the form @triviabot: [insert command]
# Needs to be further abstracted - lot of things should and will be moved to their own methods
def parse_command(command, user):
    global current_answer
    global question_in_progress
    global current_point_value
    clist = command.split(" ")
    if (not question_in_progress):
        if (clist[0] == "ask"):
            if (len(clist) > 1):
                if (clist[1] == "random"):
                    question, current_answer, category, current_point_value = get_random_question(NUM_TRIVIA_QUESTIONS)
                    question_in_progress = True
                    print current_answer
                    return format_question(category, question, current_point_value)
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
        if (command == "skip"):
            question_in_progress = False
            return "Question skipped! Answer was: " + format_string(current_answer) + "."
        if (compare_answers(command, current_answer)):
            current_answer = ""
            question_in_progress = False
            update_leaderboard(user, parse_point_value(current_point_value))
            return "Correct answer " + format_string(get_username(user)) + ". Your score is: `" + str(leaderboard[get_username(user)]) + "`."
        else:
            return "Incorrect!"

# Removes dollar sign from question amount and converts to int
def parse_point_value(points):
    try:
        return int(points[1:])
    except:
        return 0

# Compares users answer with actual answer
# Both strings are cleaned of whitespace, non alpha-numeric chars, and case
# Currently, there is no tolerance for misspelling
def compare_answers(guess, ans):
    ans = ans.split("/")
    guess = clean_answer(guess)
    for x in range(len(ans)):
        ans[x] = clean_answer(ans[x])
        if (guess == ans[x]):
            return True
    return False

# Removes all non alpha-numeric characters
def clean_answer(ans):
    ans = ans.lower()
    ans = ''.join(e for e in ans if e.isalnum())
    return ans

# Displays list of commands and descriptions
def display_help():
    res = ""
    for command in COMMANDS:
        res += format_string(command) + ": " + format_string(COMMANDS[command]) + "\n"
    return res

# Inc(dec)rements score for given user
def update_leaderboard(user, change):
    global leaderboard
    user = get_username(user)
    if user in leaderboard:
        leaderboard[user] += change
    else:
        leaderboard[user] = change
    print leaderboard

# Displays the leaderboard
def display_leaderboard():
    res = ""
    for user in leaderboard:
        res += format_string(user + ": " + str(leaderboard[user])) + "\n"
    return res

# Get a random question from the dataset
# Return question, answer, categor, and value properties
def get_random_question(size):
    c = random.randint(1,size)
    data = trivia_question_list[c]
    question = data["question"]
    category = data["category"]
    answer = data["answer"]
    value = data["value"]
    return question, answer, category, value

# Formats a string in markdown
def format_string(s):
    return "`" + s + "`"

# Formats a question, category, value combo in markdown
def format_question(category, question, value):
    return "In `" + category + "` for `" + value + "`: `" + question + "`"

# Calls parse_command and prints output to slack
def handle_command(command, channel, user):
    response = parse_command(command, user)
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

# Gets the username of a user given their userid
def get_username(user):
    return slack_client.api_call("users.info", user=user)['user']['name']

# Gets RTM text, channel, and user
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
