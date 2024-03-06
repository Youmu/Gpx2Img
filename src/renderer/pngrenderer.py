from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from datasource import telemetry

class PngImg:
    data:telemetry.NormalizedData
    BackGround : Image.Image
    Font: ImageFont.ImageFont
    TextOffset: float

    def __init__(self, data:telemetry.NormalizedData):
        self.TextOffset = 20
        self.data = data
        self.BackGround = Image.new('RGBA', (400, 400), '#00000000')
        pts = []
        for dt in self.data.DataPoints:
            pts.append((400*dt.X, 400*dt.Y))
        draw = ImageDraw.Draw(self.BackGround)
        draw.line(pts, fill='#CCCCCCFF', width=5)
        self.Font = ImageFont.truetype('./Tachyo-1.0.0.otf', size=50)
        textFont = ImageFont.truetype('Arial', size=30)
        draw.text([80,90 + self.TextOffset], 'km/h'.format(dt.SPD), fill='#EEEEEEFF', font=textFont)
        draw.text([295,90 + self.TextOffset], 'm'.format(dt.SPD), fill='#EEEEEEFF', font=textFont)

    def RenderPreview(self, filename):
        Img = Image.new('RGBA', (1024, 768), '#00000000')
        pts = []
        for dt in self.data.DataPoints:
            pts.append((400*dt.X, 400*dt.Y))
        draw = ImageDraw.Draw(Img)
        draw.line(pts, fill='#66CCFFFF', width= 4)
        for dt in self.data.DataPoints:
            draw.line(
                [(800 * dt.T, 650), (800 * dt.T, 650 - 200 * dt.E)], 
                '#66CCFFFF', 
                width=2)
        coefT = 1 / self.data.TotalSeconds
        for t in range(0, int(self.data.TotalSeconds), 60):
            draw.line(
                [(800 * (t * coefT), 650), (800 * (t * coefT), 655)],
                '#00FF00FF',
                width=1
            )
        if self.data.TotalSeconds > 3600:
            for t in range(0, int(self.data.TotalSeconds), 3600):
                draw.line(
                    [(800 * (t * coefT), 650), (800 * (t * coefT), 660)],
                    '#FFFF00FF',
                    width=5
            )
        
        Img.save(filename)

    def RenderFrame(self, path, nameprefix, time:int):
        img = self.BackGround.copy()
        draw = ImageDraw.Draw(img)
        for i in range(0, len(self.data.DataPoints) - 1, 1):
            if self.data.DataPoints[i].TimeOffset <= time and self.data.DataPoints[i+1].TimeOffset > time :
                dt = self.data.DataPoints[i]
                draw.ellipse(
                    [(dt.X * 400-8, dt.Y * 400-8),(dt.X * 400 + 8, dt.Y * 400 + 8)], 
                    fill='#00FF00FF', 
                    width=6)
                draw.text([40,40 + self.TextOffset], '{:.1f}'.format(dt.SPD), fill='#EEEEEEFF', font=self.Font, align='right')
                draw.text([250,40 + self.TextOffset], '{:.0f}'.format(dt.ELE), fill='#EEEEEEFF', font=self.Font, align='right')
                break

        path = '{p}/{prefix}{nb:04d}.png'.format(p=path, prefix=nameprefix, nb=time)
        img.save(path)
        
        
