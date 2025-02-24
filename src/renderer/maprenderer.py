from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from datasource import telemetry

class MapRenderer:
    map : Image.Image
    Lon_Width: float
    Lat_Height: float
    Lon_W : float
    Lat_N : float
    Lon_C : float
    Lat_C : float
    Border: int

    data:telemetry.TelemetryData
    BackGround : Image.Image
    Font: ImageFont.ImageFont
    TextOffset: float

    def __init__(self):
        print("Hello World!")
        self.Border = 40

    def LoadMap(self, path, Lon_W, Lon_E, Lat_N, Lat_S):
        self.map = Image.open(path)
        self.Lon_W = Lon_W
        self.Lat_N = Lat_N
        self.Lon_Width = Lon_E - Lon_W
        self.Lat_Height = Lat_N - Lat_S
        self.Lon_C = self.map.width / self.Lon_Width
        self.Lat_C = self.map.height / self.Lat_Height

    def SetData(self, data : telemetry.TelemetryData):
        self.data = data
        Top = (self.Lat_N - data.MaxLat) * self.Lat_C - self.Border
        Left = (data.MinLon - self.Lon_W) * self.Lon_C - self.Border
        Bottom = (self.Lat_N - data.MinLat) * self.Lat_C + self.Border
        Right = (data.MaxLon - self.Lon_W) * self.Lon_C + self.Border
        self.BackGround = self.map.crop((Left,Top,Right,Bottom))

    def DrawPath(self):
        Lon_W_PIC = self.data.MinLon
        Lat_N_PIC = self.data.MaxLat

        draw = ImageDraw.Draw(self.BackGround)
        pts = []
        for dt in self.data.Datapoints:
            pts.append(((dt.Lon - Lon_W_PIC) * self.Lon_C + self.Border, (Lat_N_PIC - dt.Lat) * self.Lat_C + self.Border))
        draw.line(pts, fill='#FFFFFFFF', width= 10)
        
    
    def ShowBackground(self):
        self.BackGround.show()

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
        
        
