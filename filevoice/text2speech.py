from aip import AipSpeech
import json
import re
import string
import sys

def utf8len(s):
  return len(s.encode('utf-8'))

class ClientAttributes(object):
  """
    spd	String	语速，取值0-9，默认为5中语速
    pit	String	音调，取值0-9，默认为5中语调
    vol	String	音量，取值0-15，默认为5中音量
    per	String	发音人选择, 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女
  """
  def __init__(self, spd=None, pit=None, vol=None, per=None):
    self.spd = spd
    self.pit = pit
    self.vol = vol
    self.per = per

class Client(object):
  def __init__(self, app_info_file):
    ## read app info
    with open(app_info_file, "rb") as f:
      self.app_info = json.load(f)

    APP_ID = self.app_info["app_id"]
    API_KEY = self.app_info["api_key"]
    SECRET_KEY = self.app_info["secret_key"]
    self.client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    self.attributes = ClientAttributes()

  def setConnectionTimeoutInMillis(self, ms):
    """
    ms: 建立连接的超时时间（单位：毫秒)
    """
    self.client.setConnectionTimeoutInMillis(ms)

  def setSocketTimeoutInMillis(self, ms):
    """
    ms: 通过打开的连接传输数据的超时时间（单位：毫秒）
    """
    self.client.setSocketTimeoutInMillis(ms)

  def setAttributes(self, attr):
    """
    attr: dict{str: str|int}
    """
    if "spd" in attr:
      self.attributes.spd = str(attr["spd"])
    if "pit" in attr:
      self.attributes.pit = str(attr["pit"])
    if "vol" in attr:
      self.attributes.vol = str(attr["vol"])
    if "per" in attr:
      self.attributes.per = str(attr["per"])
  
  def synthesis(self, text):
    """
    Simple synthesis of a sentence
    Return binary result, if error, print error and return None
    """
    attr = {}
    if self.attributes.spd:
      attr["spd"] = self.attributes.spd
    if self.attributes.pit:
      attr["pit"] = self.attributes.pit
    if self.attributes.vol:
      attr["vol"] = self.attributes.vol
    if self.attributes.per:
      attr["per"] = self.attributes.per

    result  = self.client.synthesis(text, 'zh', 1, attr)

    if not isinstance(result, dict):
      return result
    else:
      print("Error:", result)
      raise Exception("Stop")

  def synthesisLongString(self, text):
    """
    Divide text into pieces by end of string indicators to make sure the synthesis 
    shorter than 1024 bytes.
    Yield a generator of audio pieces
    """
    
    if utf8len(text) <= 1024:
      yield self.synthesis(text)
      return

    ## helpers for divide string into pieces and synthesis
    INDIC = "SENTEND"

    def sep(matchObj):
        return matchObj.group(1) + INDIC

    def multiShortSynthesis(text, level=1):
      first_level_indicator = ".;!? ？。！」「"
      second_level_indicator = string.punctuation + "，"
      if level == 1:
        indicators = first_level_indicator
      elif level == 2:
        indicators = second_level_indicator
      if level < 3:
        proc_text = re.sub("([" + indicators + "])", sep, text)

        split_proc = proc_text.split(INDIC)
        text_bytes = [utf8len(string) for string in split_proc]
      else:
        split_proc = text
        text_bytes = [utf8len(char) for char in split_proc]

      pointer = 0
      cur = ""
      cur_bytes = 0
    
      while pointer < len(split_proc):
        if text_bytes[pointer] > 1024:
          if cur_bytes > 0:
            yield (self.synthesis(cur))
          for audio_piece in  multiShortSynthesis(split_proc[pointer], level+1):
            yield audio_piece
        elif text_bytes[pointer] <= 1024 - cur_bytes:
          cur += split_proc[pointer]
          cur_bytes += text_bytes[pointer]
        else:
          yield (self.synthesis(cur))
          cur = split_proc[pointer]
          cur_bytes = text_bytes[pointer]
        pointer += 1
    ## run it
    for audio_piece in multiShortSynthesis(text, 1):
      yield audio_piece
    

  def synthesisFile(self, fp, storeFp, Range=None):
    """
    fp: input file pointer
    storeFp: output file pointer
    """
    data = fp.read().decode("utf8").splitlines()
    total_line = len(data)
    FROM = 1
    TO = total_line
    if Range is not None:
      FROM, TO = Range
      total_line = TO-FROM+1
    cur = ""
    cur_bytes = 0

    for c in range(FROM-1, TO+1):
      line = data[c]
      if len(line) >0:
        line_bytes = utf8len(line)
        if line_bytes + cur_bytes > 1023:
          if cur_bytes == 0:
            for audio_piece in self.synthesisLongString(line):
              storeFp.write(audio_piece)
          else:
            for audio_piece in self.synthesisLongString(cur):
              storeFp.write(audio_piece)
            cur = line
            cur_bytes = line_bytes
        else:
          cur += "\n" + line
          cur_bytes += line_bytes + 1
      sys.stdout.write("\rTransited: {0}/{1}%".format(c+1-FROM, total_line))
      sys.stdout.flush()
    print("Finished.")


    


