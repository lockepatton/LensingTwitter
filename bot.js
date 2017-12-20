console.log('The gravitational lensing bot is running.')

var Twit = require('twit');

var config = require('./config');
var T = new Twit(config);


// PART 1 GET - searching tweats
var params = {
  q: 'apod since:2017-12-18',
  count: 10
}

T.get('search/tweets', params, gotData)

function gotData(err, data, response) {
  console.log(data)
}
