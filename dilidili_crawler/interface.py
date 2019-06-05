from subprocess import call
import os
import json
import urllib.request

json_file = "dilidili.json"
if __name__=="__main__":
  target_directory = "relife"
  try:
    os.remove(json_file)
  except:
    pass
  call(["scrapy", "runspider", "dilidili.py", "-o", json_file])

  print("Starting to download.")
  fd = open(json_file)
  data = json.load(fd)
  fd.close()
  try:
    os.mkdir(target_directory)
  except Exception as e:
    print(e)
  all_count = 0
  bad = 0
  down = 0
  for video in data:
    all_count += 1
    if video.get("warn"):#bad to download
      bad+=1
      print(video.get("title") + video.get("warn") + ", the src is:" + video.get("src"))
    else:#good to download
      down +=1
  print("all:{all}, bad:{bad}, downloadable:{down}".format(all=all_count,bad=bad,down=down))
  continue_n = "o"
  while continue_n != "y" and continue_n != "n":
    continue_n = input("do download or not(y/n):")
  if continue_n == "y":
    for video in data:
      if video.get("warn"):
        print(video.get("title") + video.get("warn"))
      else:
        src = video["src"]
        title = video["title"]
        file_path = target_directory + "/"+title+".mp4"
        urllib.request.urlretrieve(src, file_path)
        print(title + " downloaded")
  elif continue_n == "n":
    print("end")

