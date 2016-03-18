import json
import os
import requests
import difflib

config = {}
mods = []

def get_config():
    global config
    try:
        config = json.loads(open("config.json").read())
    except OSError:
        print("File not found")
        return

def getmods():
  global mods
  request = requests.get(config["api_url"] + "/mod")
  mods = json.loads(request.text)["mods"]

def makedirs():
  if not os.path.exists("additions"):
    os.mkdir("additions")
  if not os.path.exists("additions/mods"):
    os.mkdir("additions/mods")
  if not os.path.exists("solder"):
    os.mkdir("solder")
  if not os.path.exists("solder/mods"):
    os.mkdir("solder/mods")

def getmatchratio(string1, string2):
  return difflib.SequenceMatcher(None, string1, string2).ratio()
    
def getmatch(file):
  matches = []
  for mod in mods:
    ratio = getmatchratio(mod, file)
    if ratio < 0.5: continue
    
    print(mod + " = " + str(ratio))
    matches.append({ratio, mod})
  
    
def package(file):
  print(file)
  getmatch(file.lower().split(".jar")[0])

def main():
  get_config()
  
  getmods()
  makedirs()
  
  for file in os.listdir("additions/mods"):
    package(file)
  
main()
