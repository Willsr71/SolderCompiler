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

def main():
  global api_url
  get_config();
  
  api_url = config["api_url"]
  
  main()