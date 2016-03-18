import json
import os
import requests

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
  print("Found mods:")
  for mod in mods:
    print(mod)

def makedirs():
  if not os.path.exists("additions"):
    os.mkdir("additions")
  if not os.path.exists("additions/mods"):
    os.mkdir("additions/mods")
  if not os.path.exists("solder"):
    os.mkdir("solder")
  if not os.path.exists("solder/mods"):
    os.mkdir("solder/mods")

def package(file):
  print(file)

def main():
  get_config()
  
  getmods()
  makedirs()
  
  print("Found files:")
  for file in os.listdir("additions/mods"):
    package(file)
  
main()
