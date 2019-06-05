var SpeechToTextV1 = require('watson-developer-cloud/speech-to-text/v1');
var LanguageTranslatorV2 = require('watson-developer-cloud/language-translator/v2');
var TextToSpeechV1 = require('watson-developer-cloud/text-to-speech/v1');
var fs = require('fs');
const Translate = require('@google-cloud/translate');
const speech = require('@google-cloud/speech');

process.env['GOOGLE_APPLICATION_CREDENTIALS']='/Users/siyuanqiu/Desktop/notes/ml/translate/siyuanTranslate-85147a50166a.json'
var speech_to_text = new SpeechToTextV1 ({
  username: 'f5947a73-9a3c-48bd-9882-71f3320ff47d',
  password: 'Nj5HDoWvQ8CJ'
});
var languageTranslator = new LanguageTranslatorV2({
  username: "daa1674f-ec7b-4d8e-9abc-267b1892c2a3",
  password: "4y4jDt1GC0XO",
  version: 'v2'
});

var text_to_speech = new TextToSpeechV1 ({
  username: 'fc4eb136-b9f5-4535-8422-53ae314a8d4e',
  password: 'uXz0JQo2TiLj'
});
// Your Google Cloud Platform project ID
const projectId = 'siyuantranslate-1520542892634';
// Creates a client
const client = new speech.SpeechClient({
  projectId: projectId,
});

// The name of the audio file to transcribe
const fileName = './file.wav';

const audioBytes = fs.createReadStream(fileName)

// The audio file's encoding, sample rate in hertz, and BCP-47 language code
const audio = {
  content: audioBytes,
};
const config = {
  encoding: 'LINEAR16',
  languageCode: 'en-US',
};
const request = {
  audio: audio,
  config: config,
};

// Detects speech in the audio file
client
  .recognize(request)
  .then(data => {
    const response = data[0];
    const transcription = response.results
      .map(result => result.alternatives[0].transcript)
      .join('\n');
    console.log(`Transcription: ${transcription}`);
  })
  .catch(err => {
    console.error('ERROR:', err);
  });