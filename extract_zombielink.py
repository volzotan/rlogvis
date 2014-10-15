import json
import urllib2

from os.path import join

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

    for gpx_id in ids:
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0'), ('Cookie', COOKIE)]

        response = opener.open("https://www.zombiesrungame.com/api/v3/user/{0}/runrecord/{1}.gpx".format(USERNAME, gpx_id))

        filename = "{0}.gpx".format(gpx_id)

        file = open(join("logs", filename), "w")
        file.write(response.read())
        file.close()

    print("written {0} GPX-Files to folder {1}".format(len(ids), FOLDER))



if __name__ == "__main__":
    download(acquire_ids())