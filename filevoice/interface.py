from text2speech import *
from convertText import *
app_info_file = "baidu_app.json"

if __name__ == "__main__":
    original_file = "盾之勇者成名录.txt"
    converted_file= "new.txt"
    audio_file = "test2.mp3"
    ## decode and encode the raw text file
    #convertANSItoUTF8(original_file, converted_file)
    text_fp = open(converted_file, 'rb')
    audio_fp = open(audio_file, "wb")

    # client
    client = Client(app_info_file)
    attr = {
      "spd": 5,
      "per": 3
    }
    client.setAttributes(attr)
    Range = (1816, 2046)
    client.synthesisFile(text_fp, audio_fp, Range)
    # data = text_fp.read().decode("utf8").splitlines()

    # for pi in client.synthesisLongString(data[1]):
    #    audio_fp.write(pi)
    text_fp.close()
    audio_fp.close()
    
