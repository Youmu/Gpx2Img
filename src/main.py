import datetime
from datasource import gpxreader, telemetry
from renderer import maprenderer, pngrenderer, isometricview, preview
import numpy as np


def RenderImgSeq(normalizedData:telemetry.NormalizedData):
    

    isom = isometricview.IsometricImg(normalizedData)
    i = 1
    fn = 1
    while i < 780:
        isom.RenderFrame('/Users/tengdayan/code/Gpx2Img/imgseq/g250215-{fn:05d}.png'.format(fn=fn), i)
        i = i + 1
        fn = fn + 1
    print(norm.DataPoints[0].Time)
    
#app = mainwindow.App()
#app.ShowMainWindow()


gpxreader = gpxreader.gpxreader()
map = maprenderer.MapRenderer()
map.LoadMap('/Users/tengdayan/code/Gpx2Img/sampledata/Nanlou.png', 126.615795,126.660673,43.424222,43.398644)
datapts = gpxreader.LoadGpx('/Users/tengdayan/code/Gpx2Img/activity.gpx')
trim = datapts.Trim(5700, 840)
norm = trim.Normalize(0.4)
map.SetData(trim)
map.DrawPath()
map.ShowBackground()
#prev = preview.RenderPreview(norm)
#prev.ShowPreview()
print('Data is from {mintime} to {maxtime}'.format(mintime = trim.MinTime, maxtime = trim.MaxTime))
print('Elevation is from {mine} to {maxe} meters'.format(mine = trim.MinEle, maxe = trim.maxEle))

#iso = isometricview.IsometricImg(norm)
#RenderImgSeq(norm)
#iso.RenderFrame('test.png', 300)


