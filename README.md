# triviabot
A slack bot for trivia questions!

## Configuration
Add a configuration file `config.py` with the following in it:
```python
SLACK_API_KEY = 'API_KEY'
TRIVIA_BOT_ID = 'BOT_ID'
```

## Questions
Currently, the questions are coming from a jeopardy JSON data set, which can be found [here](https://www.reddit.com/r/datasets/comments/1uyd0t/200000_jeopardy_questions_in_a_json_file).
