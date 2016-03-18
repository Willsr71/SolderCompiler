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

def getmatchpercentage(string1, string2):
  return int(round(difflib.SequenceMatcher(None, string1, string2).ratio() * 100))
    
def getmatch(file):
  matches = []
  top_percentage = 0
  
  for mod in mods:
    percentage = getmatchpercentage(mod, file)
    if percentage < 50: continue
    
    matches.append({"percentage": str(percentage), "mod": str(mod)})
    
    if (percentage > top_percentage):
      top_percentage = percentage
  
  print(matches)
  for match in matches:
    if match["percentage"] == str(top_percentage):
      return match["mod"]
    
def package(file):
  print(file)
  match = getmatch(file.lower().split(".jar")[0])
  print("Match: " + match)

def main():
  get_config()
  
  getmods()
  makedirs()
  
  for file in os.listdir("additions/mods"):
    package(file)
  
main()
