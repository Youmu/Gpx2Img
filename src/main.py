import datetime
from datasource import gpxreader

date = datetime.datetime.fromisoformat('2024-02-25T04:22:53.000Z')
gpxreader = gpxreader.gpxreader()

datapts = gpxreader.LoadGpx('E:\\code\\Gpx2Img\\sampledata\\activity_322887609.gpx')

print(date.tzinfo)