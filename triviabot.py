import os
import time
from slackclient import SlackClient
import config # Importing API keys and Bot ID
import random
import json
import sqlite3

# Draws questions from database
# Database is already set-up so queries are very fast

DATABASES = {
    "trivia" : "trivia.db",
    "amceight"   : "amceight.db"
}

conn = sqlite3.connect(DATABASES["trivia"])
dbc = conn.cursor()

dbc.execute('SELECT COUNT(*) FROM trivia')
NUM_TRIVIA_QUESTIONS = dbc.fetchone()[0]
conn.close()

conn = sqlite3.connect(DATABASES["amceight"])
dbc = conn.cursor()

dbc.execute('SELECT COUNT(*) FROM amceight')
NUM_AMC8_QUESTIONS = dbc.fetchone()[0]
conn.close()

BOT_ID = config.TRIVIA_BOT_ID

AT_BOT = "<@" + BOT_ID + ">:"
COMMANDS = {
    "ask random"   : "Triviabot will ask you a random trivia question.",
    "leaderboard"  : "Triviabot will display the current leaderboard.",
    "help"         : "Triviabot will list out all the commands.",
    "skip"         : "Triviabot will skip the current question.",
    "ask amc8"     : "Triviabot will ask you a random AMC 8 question"
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
                    question, current_answer, category, current_point_value = get_random_question(NUM_TRIVIA_QUESTIONS, "trivia")
                    question_in_progress = True
                    print current_answer
                    return format_question(category, question, current_point_value)
                elif (clist[1] == "amc8"):
                    question, current_answer, category, current_point_value = get_random_question(NUM_AMC8_QUESTIONS, "amceight")
                    question_in_progress = True
                    print current_answer
                    return format_link_question(category, question, current_point_value)
                else:
                    return "Invalid use of ask!"
            else:
                return "Invalid Command!"
        elif (command == "leaderboard"):
            return display_leaderboard()
        elif (command == "help"):
            return display_help()
        elif (command == "image"):
            return "http://www.gettyimages.pt/gi-resources/images/Homepage/Hero/PT/PT_hero_42_153645159.jpg"
        else:
            return "Invalid Command!"
    else:
        if (command == "skip"):
            question_in_progress = False
            return "Question skipped! Answer was: " + format_string(current_answer) + "."
        if (compare_answers(command, current_answer)):
            current_answer = ""
            question_in_progress = False
            update_leaderboard(user, current_point_value)
            return correct_answer(user)
        else:
            return incorrect_answer(user)

# Response for a correct answer
def correct_answer(user):
    username = format_string(get_username(user))
    score = str(leaderboard[get_username(user)])
    return "Correct answer " + username + ". Your score is: " + format_string(score) + "."

# Resposne for incorrect answer
def incorrect_answer(user):
    username = format_string(get_username(user))
    return "Incorrect answer " + username + "!"

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

# Displays the leaderboard
def display_leaderboard():
    res = ""
    for user in leaderboard:
        res += format_string(user + ": " + str(leaderboard[user])) + "\n"
    return res

# Get a random question from the dataset
# Return question, answer, categor, and value properties
def get_random_question(size, which_db):
    conn = sqlite3.connect(DATABASES[which_db])
    dbc = conn.cursor()
    c = random.randint(1,size)
    query = 'SELECT * FROM ' + which_db + ' WHERE q_id=' + str(c)
    dbc.execute(query)
    data = dbc.fetchone()
    conn.close()
    q_id, question, answer, category, value = data
    return question, answer, category, value

# Formats a string in markdown
def format_string(s):
    return "`" + s + "`"

# Formats a question, category, value combo in markdown
def format_question(category, question, value):
    return "In `" + category + "` for `" + str(value) + "`: `" + question + "`"

# Format a question with link (do not place link in ticks)
def format_link_question(category, question, value):
    return "In `" + category + "` for `" + str(value) + "`: " + question

# Calls parse_command and prints output to slack
def handle_command(command, channel, user):
    response = parse_command(command, user)
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

# Gets the username of a user given their userid
def get_username(user):
    return slack_client.api_call("users.info", user=user)['user']['name']

# Serves an image
def serve_image():
    return slack_client.api_call("files.upload", file="img/use_example.png", filename="use_example.png")

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
