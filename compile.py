import difflib
import json
import os

import requests

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


def get_mods():
    global mods
    request = requests.get(config["api_url"] + "/mod")
    mods = json.loads(request.text)["mods"]
    print("Got", len(mods), "mods from", config["api_url"], "\n")


def make_dirs():
    if not os.path.exists("additions"):
        os.mkdir("additions")
    if not os.path.exists("additions/mods"):
        os.mkdir("additions/mods")
    if not os.path.exists("solder"):
        os.mkdir("solder")
    if not os.path.exists("solder/mods"):
        os.mkdir("solder/mods")


def get_match_percentage(string1, string2):
    return int(round(difflib.SequenceMatcher(None, string1, string2).ratio() * 100))


def insert_match(matches, mod, percentage):
    for x in range(0, len(matches)):
        if matches[x]["percentage"] <= percentage:
            matches.insert(x, {"percentage": percentage, "mod": mod})
            return matches

    matches.append({"percentage": percentage, "mod": mod})
    return matches


def get_matches(file):
    matches = []

    file = file.split(".jar")[0]
    if not config["matching"]["case_sensitive"]:
        file = file.lower()

    for mod in mods:
        percentage = get_match_percentage(mod, file)
        # if percentage > config["matching"]["percentage_required"]:
        matches = insert_match(matches, mod, percentage)

    return matches


def prepare_packages(file):
    global packaged_files

    print("\n", file, "\n")
    matches = get_matches(file)

    max = min(5, len(matches))
    for x in range(0, max):
        print(str(x) + ". " + matches[x]["mod"] + " (" + str(matches[x]["percentage"]) + "%)")
    print(str(max) + ". Other (input)")

    use = int(input("Choose best match (0, " + str(max) + "): "))

    if use == max:
        slug = input("Enter mod slug: ")
    else:
        slug = matches[use]["mod"]

    version = input("Version: ")
    packaged_files.append({"mod_file": file, "slug": slug, "version": version})


def package_file(mod):
    if not os.path.exists("solder/mods/" + mod["slug"]):
        os.mkdir("solder/mods/" + mod["slug"])

    mod_file = mod["mod_file"]
    packaged_file = mod["slug"] + "-" + mod["version"]


def main():
    get_config()

    get_mods()
    make_dirs()

    for file in os.listdir("additions/mods"):
        prepare_packages(file)
    for mod in packaged_files:
        package_file(mod)


main()
