import datetime
from datasource import gpxreader
from renderer import pngrenderer

date = datetime.datetime.fromisoformat('2024-02-25T04:22:53.000Z')
gpxreader = gpxreader.gpxreader()

datapts = gpxreader.LoadGpx('E:\\code\\Gpx2Img\\sampledata\\activity_322887609.gpx')
norm = datapts.Normalize()
print('Data is from {mintime} to {maxtime}'.format(mintime = datapts.MinTime, maxtime = datapts.MaxTime))
print('Elevation is from {mine} to {maxe} meters'.format(mine = datapts.MinEle, maxe = datapts.maxEle))
print(date.tzinfo)
trim = norm.Trim(420, 480)
r = pngrenderer.PngImg(trim)
r.RenderPreview('test.png')
for i in range(1, 400):
    r.RenderFrame('E:\\code\\output', 'frame', i)
print(norm.DataPoints[0].Time)