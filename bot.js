console.log('The gravitational lensing bot is running.')

var Twit = require('twit');
var exec = require('child_process').exec;
var fs = require('fs');

var config = require('./config');
var T = new Twit(config);

// Running tweetIt every 24 hours
tweetIt()
// setInterval(tweetIt, 1000*60*5*60*24) //# of mili-seconds


function tweetIt() {

  // Gets APOD Image and Lenses It
  // Executes this process in python
  var cmd = 'python ./lensAPOD.py';
  exec(cmd, processing)

  // Once executed, runs processes
  function processing() {
    console.log('1: If it exists, the APOD image was found and lensed in Python.')

    // Reading in image
    filename = './pictures/AstroPicOfTheDay_Lensed.jpg'
    var params = {
      encoding: 'base64'
    }
    var b64 = fs.readFileSync(filename, params);
    console.log('2: Image imported with readFileSync.')

    // uploading media to account
    T.post('media/upload', {media_data: b64}, uploaded);

    function uploaded(err, data, response) {
      if (err) {
        console.log(err);
      } else {
        var id = data.media_id_string;
        var tweet = {
          status: '#CodingRainbow',
          media_ids: [id]
        }
        T.post('statuses/update', tweet, tweeted);
      }
    }
  }

  function tweeted(err, data, response) {
      if (err) {
        console.log("Error appeared!");
      } else {
        console.log("3: Tweet successful!");
      }
    }
}
