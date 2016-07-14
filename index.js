// Imports
var SlackBot = require('slackbots');
var config = require('./config.json');
var properties = require('./properties.json');
var request = require('request');
// State variables
QUESTION_CACHE = {}

// create a bot
var bot = new SlackBot({
    token: config['api_key'],
    name: properties['name']
});

bot.on('start', function() {
    console.log(properties['name'] + 'starting up!');

    ask_random();

    // define channel, where bot exist. You can adjust it there https://my.slack.com/services
    // bot.postMessageToChannel('trivia', 'Hello, I am triviabot!');
});

bot.on('message', function(data) {
  console.log(data);
  if (data['text'] && data['user'] != properties['botid']) {
    var message = data['text'];
    var response = parse(message);
    bot.postMessageToChannel('trivia', response);
  };

});

// Functions
function parse(msg) {
  if (msg.substring(0,10) == 'triviabot ') {
    var command = msg.substring(10).split(' ');
    try {
      if (command[0] == 'ask') {
        if (command[1] == 'random') {
          return QUESTION_CACHE;
        };
      };
    }
    catch(err) {
      return 'Invalid command!';
    };
  }
  else {
    return 'Address me with "triviabot" please.';
  };
};

function ask_random() {
  request('http://www.jservice.io/api/random?count=2', function (error, response, body) {
    if (!error && response.statusCode == 200) {
      body =  JSON.parse(body)[0];
      for (var i = 0; i < body.length; i ++) {
        tmp = {}
        tmp["question"] = body[i].question;
        tmp["answer"] = body[i].answer;
        tmp["category"] = body[i].category.title;
        QUESTION_CACHE[i] = tmp;
      };
      // var response = 'Category: `' + category + '` Question: `' + question + '`';
      // console.log(response);
    };
  });
};
