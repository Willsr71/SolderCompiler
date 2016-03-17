import json
import os
import requests

config = {}
api_url = ""

def get_config():
    global config
    try:
        config = json.loads(open("config.json").read())
    except OSError:
        print("File not found")
        return

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
  global api_url
  get_config()
  
  api_url = config["api_url"]
  makedirs()
  
  for file in os.listdir("additions/mods"):
    package(file)
  
main()
