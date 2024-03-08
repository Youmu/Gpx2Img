import datetime
from datasource import gpxreader
from renderer import pngrenderer
from renderer import isometricview
import numpy as np

gpxreader = gpxreader.gpxreader()

datapts = gpxreader.LoadGpx('/Users/tengdayan/Code/data/activity_325365050.gpx')
norma = datapts.Normalize(1)
print('Data is from {mintime} to {maxtime}'.format(mintime = datapts.MinTime, maxtime = datapts.MaxTime))
print('Elevation is from {mine} to {maxe} meters'.format(mine = datapts.MinEle, maxe = datapts.maxEle))

trimmeddpts = datapts.Trim(1638, 180)
norm = trimmeddpts.Normalize(0.4)
#trim = norm.Trim(1668, 90) #3906/780
r = pngrenderer.PngImg(norma)
r.RenderPreview('test.png')
r.RenderFrame('.', 'sample', 30)

isom = isometricview.IsometricImg(norm)
isom.RenderPreview('isometric.png')
isom.RenderFrame('.', 'sampleiso', 30, 1)
i = 1
fn = 1
while i < 150:
    isom.RenderFrame('/Users/tengdayan/Code/output', 'g122132-', i, fn)
    i = i + 0.2
    fn = fn + 1
#for i in range(1, 780):
#    r.RenderFrame('/Users/tengdayan/Code/output', 'f105526-', i)
print(norm.DataPoints[0].Time)