console.log('The gravitational lensing bot is running.')

var Twit = require('twit');
var exec = require('child_process').exec;
var fs = require('fs');
var ontime = require('ontime')

var config = require('./config');
var T = new Twit(config);

const fileExists = require('file-exists');

// 1st PROCESS: Reply with lensed images!

var stream = T.stream('user');

stream.on('tweet', tweetEvent)

function tweetEvent(eventMsg) {
  // WRITING eventMsg TO JSON FILE
  var json = JSON.stringify(eventMsg, null, 2);
  fs.writeFile("tweet.json", json, (error) => { /* handle error */ });

  var AllImages = []
  var AllImages_Lensed = []

  var replyto = eventMsg.in_reply_to_screen_name;
  var text = eventMsg.text;
  var nameID = eventMsg.id_str;
  var from = eventMsg.user.screen_name;

  // Finding their image(s) / gif 1st image (need to test video)
  if (replyto == 'TheLensBot' && eventMsg.extended_entities != null) {
    for (i = 0; i < eventMsg.extended_entities.media.length; i++) {
      var type = eventMsg.extended_entities.media[i].type;
      if (type == 'photo') {
        console.log(type);
      }
      var pictureLink = eventMsg.extended_entities.media[i].media_url_https;
      AllImages.push(pictureLink)
    }
  }

  // Finding re-tweet image(s) / gif 1st image (need to test video)
  if (replyto == 'TheLensBot' && eventMsg.quoted_status != null) {
    for (i = 0; i < eventMsg.quoted_status.extended_entities.media.length; i++) {
      var type = eventMsg.quoted_status.extended_entities.media[i].type;
      if (type == 'photo') {
        console.log(type);
      }
      var pictureLink = eventMsg.quoted_status.extended_entities.media[i].media_url_https;
      AllImages.push(pictureLink)
    }
  }

  console.log(AllImages)
  console.log('successfully found images');

  imageLocationStr = ''
  for (i = 0; i < AllImages.length; i++) {
    imageLocationStr = imageLocationStr + ' ' + AllImages[i]
    AllImages_Lensed.push('./pictures/Image'+i+'_Lensed.jpg')
  }

  var cmd_removeOldImages = 'rm  ./pictures/Image*Lensed*';
  var cmd = 'python ./lensImage.py ' + AllImages.length + imageLocationStr;

  if (AllImages_Lensed.length > 0) {
    // Running all lensing processes lensImage.py for all attached images
    // exec(cmd_removeOldImages,printRemovedImages)
    exec(cmd,tweetImages)
  }

  function printRemovedImages() {
    console.log('Removed old @images.')
  }

  function tweetImages() {
    console.log('1: lensImage.py program run for all images. If they exist, they were downloaded and lensed in Python.')

    console.log(AllImages_Lensed)

    for (i = 0; i < AllImages_Lensed.length; i++) {
      // Reading in image
      filename = AllImages_Lensed[i]
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
            status: '@'+from+' Some extra gravity on the situation!',
            media_ids: [id],
            in_reply_to_status_id: nameID
          }
          T.post('statuses/update', tweet, tweeted);

          function tweeted(err, data, response) {
              if (err) {
                console.log("Error appeared!");
                console.log(response);
              } else {
                console.log("3: Tweet successful!");
              }
            }
        }
      }
    }
  }
}


// 2nd PROCESS: Lens the AstroPicOfTheDay!

// Running mainAPOD every 24 hours
// mainAPOD()
// setInterval(mainAPOD, 1000*60*60*24) //delay time in milli-seconds

// Post at 5pm every day
ontime({ cycle: '22:00:00' }, mainAPOD)

// Gets APOD Image, and if it exists it will lenses It, and tweet it.
function mainAPOD() {
  // Running lensAPOD.py
  var cmd = 'python ./lensAPOD.py';
  var cmd_removeOldImages = 'rm  ./pictures/AstroPicOfTheDay*Lensed*';

  // exec(cmd_removeOldImages,printRemovedImages)
  exec(cmd, lensAPOD)

  function printRemovedImages() {
    console.log('Removed old APOD images.')
  }

  // Once executed, runs processing
  function lensAPOD() {
    console.log('1: lensAPOD.py run. If it exists, the APOD image was found and lensed in Python.')

    // Testing if file exists, and if it does, running tweetIt
    var file = './pictures/AstroPicOfTheDay_Lensed.jpg';
    fileExists(file, tweetAPOD)

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
              status: 'A gravitationally lensed #astro picture of the day! #apod '+ getDateLinkAPOD(),
              media_ids: [id]
            }

            function getDateLinkAPOD() {
              var date = new Date();

              var yearCut = date.getFullYear() - 2000;
              var month = date.getMonth() + 1;
              var day = date.getDate() + 1;
              var siteDite = 'https://apod.nasa.gov/apod/ap'+yearCut +''+ month +''+ day + '.html';

              return siteDite;
            }

            T.post('statuses/update', tweet, tweeted);

            function tweeted(err, data, response) {

                if (err) {
                  console.log("Error appeared!");
                  console.log(response);

                } else {
                  console.log("3: Tweet successful!");
                }
              }
          }
        }
      }
    }
  }
}
