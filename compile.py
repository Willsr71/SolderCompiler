import json
import os
import requests
import difflib

config = {}
mods = []
packaged_files = []

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
    
def gettopmatches(file):
  matches = []
  top_percentages = [0]
  
  file = file.split(".jar")[0]
  if not config["matching"]["case_sensitive"]:
    file = file.lower()
  
  for mod in mods:
    percentage = getmatchpercentage(mod, file)
    if percentage < config["matching"]["percentage_required"]: continue
    
    matches.append({"percentage": str(percentage), "mod": str(mod)})
    
    for x in range(0, len(top_percentages)):
      if percentage > top_percentages[x]:
        top_percentages.add(percentage)
  
  print("Top percentages", top_percentages)
  print("Matches", matches)
  top_matches = []
  
  for match in matches:
    if match["percentage"] in top_percentages:
      top_matches.append(match["mod"])
  
  print("Top matches", top_matches)
  return top_matches
    
def prepare_packages(file):
  global packaged_files
  
  print(file)
  top_matches = gettopmatches(file)
  print(top_matches)
  
  for x in range(0, 4):
    print("Mod file:   " + file)
    print("Best match: " + top_matches[x])
    use = print("Use this match?")
    if (use):
      version = print("Version?")
      packaged_files.append({"mod_file": file, "slug": top_matches[x], "version": version})
      return
  
  slug = print("No matches found. Please enter mod slug.")
  version = print("Version?")
  packaged_files.append({"mod_file": file, "slug": slug, "version": version})

def package_file(mod):
  if not os.path.exists("solder/mods/" + mod["slug"]):
    os.mkdir("solder/mods/" + mod["slug"])
  
  mod_file = mod["mod_file"]
  packaged_file = mod["slug"] + "-" + mod["version"]
  

def main():
  get_config()
  
  getmods()
  makedirs()
  
  for file in os.listdir("additions/mods"):
    prepare_packages(file)
  for mod in packaged_files:
    package_file(mod)
  
main()
