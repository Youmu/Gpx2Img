from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from datasource import telemetry

class PngImg:

    def __init__(self, width, height):
        self.Width = width
        self.Height = height
        self.Img = Image.new('RGBA', (width, height), '#00000000')

    def RenderTrack(self, data:telemetry.NormalizedData):
        pts = []
        for dt in data.DataPoints:
            pts.append((400*dt.X, 400*dt.Y))
        draw = ImageDraw.Draw(self.Img)
        draw.line(pts, fill='#66CCFFFF', width= 4)

    def RenderProfile(self, data:telemetry.NormalizedData):  
        draw = ImageDraw.Draw(self.Img)      
        for dt in data.DataPoints:
            draw.line(
                [(800 * dt.T, 650), (800 * dt.T, 650 - 200 * dt.E)], 
                '#66CCFFFF', 
                width=2)
        coefT = 1 / data.TotalSeconds
        for t in range(0, int(data.TotalSeconds), 60):
            draw.line(
                [(800 * (t * coefT), 650), (800 * (t * coefT), 655)],
                '#00FF00FF',
                width=1
            )
    def SaveToFile(self, filename):
        self.Img.save(filename)
        
