module.exports = {

  parse: function(msg) {
    if (msg.substring(0,10) == 'triviabot ') {
      var command = msg.substring(10).split(' ');
      console.log(command);
      try {
        if (command[0] == 'ask') {
          if (command[1] == 'random') {
            module.exports.ask_random();
            return "no";
          };
        };
      }
      catch(err) {
        console.log(err);
        return 'Invalid command!';
      };
    }
    else {
      return 'Address me with "triviabot" please.';
    };
  },

  ask_random: function() {
    request('http://www.jservice.io/api/random', function (error, response, body) {
      if (!error && response.statusCode == 200) {
        console.log(response); // Show the HTML for the Google homepage.
      };
    });
  }


};
