import json
import os
import sys
import glob
import re
from collections import OrderedDict

configmap_file_name = sys.argv[1]
current_calling_directory = sys.argv[2]
# change working directory to caller's directory
os.chdir(current_calling_directory)
configmap_json_object={}
_from_file_arg = os.environ.get("KUBECTL_PLUGINS_LOCAL_FLAG_FROM_FILE")
_add_field_value = os.environ.get("KUBECTL_PLUGINS_LOCAL_FLAG_ADD")
_delete_field = os.environ.get("KUBECTL_PLUGINS_LOCAL_FLAG_DELETE")

def add_file_content_into_configmap_json(_from_file_arg):
  # check if field name is specified --from-file={fieldname}={path_to_file}
  _arg_map = _from_file_arg.split("=")
  if len(_arg_map) == 1: # field name will be the file name
    abspath = os.path.abspath(_arg_map[0])
    if os.path.isdir(abspath): # a whole dir
      for _file in os.listdir(abspath):
        filepath = os.path.join(abspath, _file)
        if os.path.isfile(filepath):
          change_field_from_file_content(_file, filepath)
    elif "*" in abspath: # wild card
      for _file in glob.glob(abspath): # this returns the abs path of the file
        if os.path.isfile(_file):
          file_name = os.path.basename(_file)
          change_field_from_file_content(file_name, _file)
    elif os.path.isfile(abspath): # a single file
      file_name = os.path.basename(abspath)
      change_field_from_file_content(file_name, abspath)
    else:
      print(_arg_map[0] + " file does not exist or does not contain valid files")
      sys.exit(1)
  else: # field name is specified, only one file
    field_name = _arg_map[0]
    abspath = os.path.abspath(_arg_map[1]) 
    change_field_from_file_content(field_name, abspath)

def add_field_value_pair_into_configmap_json(_pair):
  # Valid pair must be `key=value`
  # Split only the first `=`, sequential `=`s are regarding as part of value
  _pair_key_value = _pair.split("=", 1)
  if len(_pair_key_value) != 2:
    print(_pair + " is not valid pair, use --add={field}={value}")
    sys.exit(1)
  else:
    field = _pair_key_value[0]
    value = _pair_key_value[1]
    change_field(field, value)

def delete_field_from_configmap_json(_field):
  # Delete the field if exist, if not exist, print message
  value = delete_field(_field)
  if not value: # None, print not exist message
    print(_field + " does not exit, not deleting.")
  else:
    print(_field + " deleted")
    
def main():
  global configmap_json_object
  global configmap_file_name
  # load the main json object from configmap temp json file
  configmap_json_object = readJson(configmap_file_name)
  if not configmap_json_object:
    print(configmap_file_name + " does not have correct content")
    sys.exit(1)
  # handle --from-file arguments
  if _from_file_arg:
    # split this arg by comma ","
    _from_file_arg_list=_from_file_arg.split(",")
    for _arg in _from_file_arg_list:
      add_file_content_into_configmap_json(_arg)
  # handle --add arguments
  if _add_field_value:
    add_field_value_pair_into_configmap_json(_add_field_value)
  # handle --delete
  if _delete_field:
    _delete_field_list = _delete_field.split(",")
    for _arg in _delete_field_list:
      delete_field_from_configmap_json(_arg)
  writeJsonToFile(configmap_json_object, configmap_file_name)

#=============================================================================#
#------------------------------helper functions-------------------------------#
#=============================================================================#
def writeJsonToFile(json_object, file_name):
  """
    write the json object into given file_name
  """
  fp = open(file_name, "w")
  json.dump(json_object, fp, indent=2)
  fp.close()

def readJson(file_name):
  """
    return a json object by given file name
  """
  fp = open(file_name, "r")
  content = json.load(fp, object_pairs_hook=OrderedDict)
  fp.close()
  return content

def change_field_from_file_content(field_name, file_name):
  """
    change json field with content by given file 
  """
  fp = open(file_name, "r")
  content = fp.read()
  change_field(field_name, content)

def change_field(field_name, value):
  """
    base function of changing json field value
  """
  global configmap_json_object
  configmap_json_object["data"][field_name] = value
  
def delete_field(field_name):
  """
    base function of deleting a field, 
    return the value if exist, otherwise return None
  """
  global configmap_json_object
  return configmap_json_object["data"].pop(field_name, None)

if __name__=="__main__":
  main()