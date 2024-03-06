from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from datasource import telemetry

class IsometricImg:
    data:telemetry.NormalizedData
    BackGround : Image.Image
    Font: ImageFont.ImageFont
    TextOffset: float

    def __init__(self, data:telemetry.NormalizedData):
        self.TextOffset = 60
        self.data = data
        self.BackGround = Image.new('RGBA', (400, 400), '#00000000')
        pts1 = []
        pts2 = []
        draw = ImageDraw.Draw(self.BackGround)
        for dt in self.data.DataPoints:
            p1 = (400*dt.X, 200*dt.Y + 200)
            p2 = (400*dt.X, 200*dt.Y + 200 - 100 * dt.E)
            pts1.append(p1)
            pts2.append(p2)
        draw.line(pts1, fill='#CCCCCCFF', width=5)
        for dt in self.data.DataPoints:
            p1 = (400*dt.X, 200*dt.Y + 200)
            p2 = (400*dt.X, 200*dt.Y + 200 - 100 * dt.E)
            draw.line([p1, p2],fill='#CCCCCC88', width=1)
        draw.line(pts2, fill='#CCCCCCFF', width=5)

        self.Font = ImageFont.truetype('/Users/tengdayan/Code/Gpx2Img/Tachyo-1.0.0.otf', size=50)
        textFont = ImageFont.truetype('Arial', size=30)
        draw.text([80,90 + self.TextOffset], 'km/h'.format(dt.SPD), fill='#EEEEEEFF', font=textFont)
        draw.text([295,90 + self.TextOffset], 'm'.format(dt.SPD), fill='#EEEEEEFF', font=textFont)

    def RenderPreview(self, filename):
        self.BackGround.save(filename)

    def RenderFrame(self, path, nameprefix, time:int):
        img = self.BackGround.copy()
        draw = ImageDraw.Draw(img)
        for i in range(0, len(self.data.DataPoints) - 1, 1):
            if self.data.DataPoints[i].TimeOffset <= time and self.data.DataPoints[i+1].TimeOffset > time :
                dt = self.data.DataPoints[i]
                X = 400*dt.X
                Y = 200*dt.Y + 200 - 100 * dt.E
                draw.ellipse(
                    [(X - 8, Y - 8),(X + 8, Y + 8)], 
                    fill='#00FF00FF', 
                    width=6)
                draw.text([40,40 + self.TextOffset], '{:.1f}'.format(dt.SPD), fill='#EEEEEEFF', font=self.Font, align='right')
                draw.text([250,40 + self.TextOffset], '{:.0f}'.format(dt.ELE), fill='#EEEEEEFF', font=self.Font, align='right')
                break

        path = '{p}/{prefix}{nb:04d}.png'.format(p=path, prefix=nameprefix, nb=time)
        img.save(path)
        
        
