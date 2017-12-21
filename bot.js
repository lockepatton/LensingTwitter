console.log('The gravitational lensing bot is running.')

var Twit = require('twit');
var exec = require('child_process').exec;
var fs = require('fs');

var config = require('./config');
var T = new Twit(config);

const fileExists = require('file-exists');

// Gets APOD Image, and if it exists it will lenses It, and tweet it.
mainAPOD()
// Running mainAPOD every 24 hours
setInterval(mainAPOD, 1000*60*5*60*24) //delay time in milli-seconds


function mainAPOD() {
  // Running lensAPOD.py
  var cmd = 'python ./lensAPOD.py';
  exec(cmd, lensAPOD)
}

// Once executed, runs processing
function lensAPOD() {
  console.log('1: lensAPOD.py run. If it exists, the APOD image was found and lensed in Python.')

  // Testing if file exists, and if it does, running tweetIt
  var file = '/Users/lockepatton/LensingTwitter/pictures/AstroPicOfTheDay_Lensed.jpg';
  fileExists(file, tweetAPOD)
}

function tweetAPOD(err, exists) {
  console.log(exists);
  if (exists) {
    console.log("The file exists. Continuing.")
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

        function tweeted(err, data, response) {
            if (err) {
              console.log("Error appeared!");
            } else {
              console.log("3: Tweet successful!");
            }
          }
      }
    }
  }
}
