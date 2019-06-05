var SpeechToTextV1 = require('watson-developer-cloud/speech-to-text/v1');
var TextToSpeechV1 = require('watson-developer-cloud/text-to-speech/v1');
var fs = require('fs');
const Translate = require('@google-cloud/translate');

process.env['GOOGLE_APPLICATION_CREDENTIALS']='/Users/siyuanqiu/Desktop/notes/ml/translate/siyuanTranslate-85147a50166a.json'
var speech_to_text = new SpeechToTextV1 ({
  username: 'f5947a73-9a3c-48bd-9882-71f3320ff47d',
  password: 'Nj5HDoWvQ8CJ'
});

// Your Google Cloud Platform project ID
const projectId = 'siyuantranslate-1520542892634';

// Instantiates a client
const translate = new Translate({
  projectId: projectId,
});

var text_to_speech = new TextToSpeechV1 ({
  username: 'fc4eb136-b9f5-4535-8422-53ae314a8d4e',
  password: 'uXz0JQo2TiLj'
});

var modelList = {};
speech_to_text.listModels(null, function(error, models) {
  if (error)
    console.log('Error:', error);
  else
    modelList = models;
});
file = 'file.wav';
var params = {
  audio: fs.createReadStream(file),
  content_type: 'audio/wav',
  model: 'en-US_BroadbandModel',
  max_alternatives: 3 ,
};
var confidence = 0;
var transcript = '';
speech_to_text.recognize(params, function(error, data) {
  if (error)
    console.log('Error:', error);
  else
    confidence =  data.results[0].alternatives[0].confidence;
    console.log(`The confidence is ${confidence}`);
    if(confidence < 0.2){
      console.log("Can not recognize! please speak again.");
      return;
    }
    var text = data.results[0].alternatives[0].transcript;
    console.log(`Text: ${text}`);
    var target = "ja";
    translate
      .translate(text, target)
      .then(results => {
        const translation = results[0];
        console.log(`Translation: ${translation}`);
        var params = {
          text: translation,
          voice: 'ja-JP_EmiVoice',
          accept: 'audio/wav'
        };
        // Pipe the synthesized text to a file.
        text_to_speech.synthesize(params).on('error', function(error) {
          console.log('Error:', error);
        }).pipe(fs.createWriteStream('out.wav'));
      })
      .catch(err => {
        console.error('ERROR:', err);
    });
});

