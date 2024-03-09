from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from datasource import telemetry

class RenderPreview:
    data:telemetry.NormalizedData
    Preview : Image.Image
    Font: ImageFont.ImageFont

    def __init__(self, data:telemetry.NormalizedData):
        self.data = data
        self.Font = ImageFont.truetype('Arial', size=30)
        

    def ShowPreview(self):
        self.Preview = Image.new('RGBA', (800, 1100), '#000000FF')
        pts = []
        for dt in self.data.DataPoints:
            pts.append((400*dt.X + 400, 400 - 400*dt.Y))
        draw = ImageDraw.Draw(self.Preview)
        draw.line(pts, fill='#66CCFFFF', width=1)

        for dt in self.data.DataPoints:
            draw.line(
                [(800 * dt.T, 1050), (800 * dt.T, 1050 - 200 * dt.Z)], 
                '#66CCFFFF', 
                width=1)
            
        coefT = 1 / self.data.TotalSeconds
        for t in range(0, int(self.data.TotalSeconds), 60):
            draw.line(
                [(800 * (t * coefT), 1050), (800 * (t * coefT), 1055)],
                '#00FF00FF',
                width=1
            )
        if self.data.TotalSeconds > 600:
            for t in range(0, int(self.data.TotalSeconds), 600):
                draw.line(
                    [(800 * (t * coefT), 1050), (800 * (t * coefT), 850)],
                    '#FFFFFFFF',
                    width=1
            )
        self.Preview.show()

