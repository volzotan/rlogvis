import gpxpy
import gpxpy.gpx

from jinja2 import Environment, FileSystemLoader, Template

from os import listdir
from os.path import isfile, join

import sys
import subprocess, os

import json

def extract(file_names):
    data = []

    for name in file_names:
        run = {}

        gpx_file = open(name, 'r')
        gpx = gpxpy.parse(gpx_file)

        for track in gpx.tracks:
            for segment in track.segments:
                position = 0
                for i in range(1, len(segment.points)):
                    try:
                        segment.points[i].speed = float(segment.points[i-1].speed_between(segment.points[i])) * 3.6
                    except:
                        segment.points[i].speed = 0

                    segment.points[i].distance = gpxpy.geo.distance(segment.points[i-1].latitude, segment.points[i-1].longitude, 0, segment.points[i].latitude, segment.points[i].longitude, 0)
                    position += segment.points[i].distance
                    segment.points[i].position = position

                segment.points[0].position = position
                segment.points[0].distance = 0
                segment.points[0].speed = 0

        datasets = []

        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    datasets.append([point.position, point.distance, point.speed])

        run["name"] = name
        run["time"] = int(gpx.tracks[0].segments[0].points[0].time.strftime("%s")) * 1000
        run["data"] = datasets

        data.append(run)
    return data

# distance = 0
# speed = 0

# for track in gpx.tracks:
#     for segment in track.segments:
#         for point in segment.points:
#             print("{}, {}".format(point.distance, point.speed))
#             distance += point.distance
#             speed += point.speed * distance

# print("{0}km, {1}km/h".format(round(distance / 1000,2), round((speed / distance)/1000,4)))
        
files = [ join("logs",f) for f in listdir("logs") if isfile(join("logs",f)) and ".gpx" in f ]
files = files #[:5]
context = {"rundata_dump": json.dumps(extract(files))}

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('template.html')

output = "output.html"

file = open(output, 'w')
file.write(template.render(context))
file.close()

# open output file
if sys.platform.startswith('darwin'):
    subprocess.call(('open', output))
elif os.name == 'nt':
    os.startfile(output)
elif os.name == 'posix':
    subprocess.call(('xdg-open', output))
