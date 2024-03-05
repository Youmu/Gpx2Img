import datetime
from datasource import gpxreader
from renderer import pngrenderer

gpxreader = gpxreader.gpxreader()

datapts = gpxreader.LoadGpx('/Users/tengdayan/Code/data/activity_325331051.gpx')
norm = datapts.Normalize()
print('Data is from {mintime} to {maxtime}'.format(mintime = datapts.MinTime, maxtime = datapts.MaxTime))
print('Elevation is from {mine} to {maxe} meters'.format(mine = datapts.MinEle, maxe = datapts.maxEle))

trim = norm.Trim(3960, 780)
r = pngrenderer.PngImg(trim)
r.RenderPreview('test.png')
r.RenderFrame('.', 'sample', 30)
for i in range(1, 780):
    r.RenderFrame('/Users/tengdayan/Code/output', 'f105526-', i)
print(trim.DataPoints[0].Time)