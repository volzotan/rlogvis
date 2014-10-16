import json
import urllib2

from os.path import join, isfile

USERNAME = ""
COOKIE = ""

FOLDER = "logs"

def acquire_ids():

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0'), ('Cookie', COOKIE)]
    response = opener.open("https://www.zombiesrungame.com/api/v3/user/{0}/runrecord/?limit=0&depth=shallow&short=true".format(USERNAME))

    data = json.load(response)

    ids = []
    for elem in data["objects"]:
        ids.append(elem["id"])

    print("found {0} IDs".format(len(ids)))

    return ids


def download(ids):

    print("retrieving files ...")

    duplicates = 0

    for gpx_id in ids:
        if not isfile(join(FOLDER, str(gpx_id) + ".gpx")):
            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0'), ('Cookie', COOKIE)]

            response = opener.open("https://www.zombiesrungame.com/api/v3/user/{0}/runrecord/{1}.gpx".format(USERNAME, gpx_id))

            filename = "{0}.gpx".format(gpx_id)

            file = open(join(FOLDER, filename), "w")
            file.write(response.read())
            file.close()
        else:
            duplicates += 1

    print("written {0} GPX-Files to folder {1} and omitted {2} duplicates".format(len(ids)-duplicates, FOLDER, duplicates))



if __name__ == "__main__":
    download(acquire_ids())