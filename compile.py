import difflib
import json
import os
import shutil

import requests
import util

from util import print_line

config = util.get_json_file("config.json")
mods = []


def get_mods():
    global mods
    request = requests.get(config["api_url"] + "/mod")
    mods = json.loads(request.text)["mods"]
    print("Got", len(mods), "mods from", config["api_url"], "\n")


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def make_dirs():
    make_dir("additions/mods")
    make_dir("added/mods")
    make_dir("solder/mods")


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
        matches = insert_match(matches, mod, percentage)

    return matches


def package_file(mod):
    make_dir("solder/mods/" + mod["slug"])
    make_dir("temp/mods")

    mod_file = mod["mod_file"]
    packaged_file = mod["slug"] + "/" + mod["slug"] + "-" + mod["version"]

    print_line("Archiving... ")
    shutil.copyfile("additions/mods/" + mod_file, "temp/mods/" + mod_file)
    shutil.make_archive("solder/mods/" + packaged_file, 'zip', "temp")
    shutil.move("additions/mods/" + mod_file, "added/mods/" + mod_file)
    shutil.rmtree("temp")
    print_line("Done.\n")


def prepare_packages(file):
    global packaged_files

    print("\n", file, "\n")
    matches = get_matches(file)

    max = min(5, len(matches))
    for x in range(0, max):
        print(str(x) + ". " + matches[x]["mod"] + " (" + str(matches[x]["percentage"]) + "%)")
    print(str(max) + ". Other (input)")

    use = input("Choose best match (0, " + str(max) + "): ")

    if use == "":
        use = 0
    else:
        use = int(use)

    if use == max:
        slug = input("Enter mod slug: ")
    else:
        slug = matches[use]["mod"]

    version = input("Version: ")
    package_file({"mod_file": file, "slug": slug, "version": version})


def main():
    get_mods()
    make_dirs()

    while len(os.listdir("additions/mods")) != 0:
        prepare_packages(os.listdir("additions/mods")[0])


main()
