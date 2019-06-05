import html

def convertANSItoUTF8(file_name, output_file):

  with open(file_name, "rb") as f:
    data = f.read().decode('GBK')

  with open(output_file, "wb") as f:
    f.write(html.unescape(data).encode("utf8"))
