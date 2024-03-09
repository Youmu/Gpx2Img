from PIL import Image, ImageColor, ImageDraw, ImageFont
import math
import numpy as np
from datasource import telemetry

class Polygon:
    Depth: float
    Points: np.matrix
    def __init__(self, Points:np.matrix):
        self.Points = Points
        self.Depth = sum(Points[:,1])[0,0] / len(Points)

    def RefreshDepth(self):
        self.Depth = sum(self.Points[:,1])[0,0] / len(self.Points)


class CourseData:
    Course: np.matrix
    Polygons: list[Polygon]
    Shadow: np.matrix
    Rotation: np.matrix
    MaxX: float
    MaxY: float

    Rows: int
    def __init__(self, data:telemetry.NormalizedData):
        pt0 = np.array([data.DataPoints[0].X, data.DataPoints[0].Y, data.DataPoints[0].Z])
        datalen = len(data.DataPoints)
        ptlist = []
        self.Rows = 0
        self.MaxX = 0
        self.MaxY = 0
        for i in range(1, datalen):
            dpt = data.DataPoints[i]
            pti = np.array([dpt.X, dpt.Y, dpt.Z])
            if np.linalg.norm(pti - pt0) < 0.05 : continue
            pt0 = pti
            if dpt.X > self.MaxX: self.MaxX = dpt.X
            if dpt.Y > self.MaxY: self.MaxY = dpt.Y
            ptlist.append(pti)
            self.Rows += 1
        self.Course = np.matrix(ptlist)
        self.CourseToPolygons()
        self.Shadow = self.Course.copy()
        self.Shadow[:,2] = 0

    def SetRotationMatrix(self, alpha, beta, imageScale):
        """Rotate along Z axis for alpha rad. Then along X azis for beta rad."""
        sa = math.sin(alpha)
        ca = math.cos(alpha)
        sb = math.sin(beta)
        cb = math.cos(beta)
        rot1 = np.matrix([[ ca, sa, 0],
                          [-sa, ca, 0],
                          [  0,  0, 1]])
        
        rot2 = np.matrix([[ 1,   0,  0],
                          [ 0,  cb, sb],
                          [ 0, -sb, cb]])
        
        scale3 = np.matrix([[ imageScale, 0, 0],
                            [ 0, imageScale, 0],
                            [ 0, 0, 0.0-imageScale]])
        
        self.Rotation = np.dot(np.dot(rot1, rot2), scale3)
        return self.Rotation
    
    def Projection(self, point):
        p = np.dot(point, self.Rotation)
        return (p[0,0] + 200, p[0,2] + 350)

    def CourseToPolygons(self):
        self.Polygons = []
        ptNumbers = len(self.Course)
        for i in range(1, ptNumbers):
            polygon = []
            polygon.append([self.Course[i-1,0], self.Course[i-1,1], 0])
            polygon.append([self.Course[i-1,0], self.Course[i-1,1], self.Course[i-1,2]])
            polygon.append([self.Course[i,  0], self.Course[i,  1], self.Course[i,2]])
            polygon.append([self.Course[i,  0], self.Course[i,  1], 0])
            self.Polygons.append(Polygon(np.matrix(polygon)))

    def Draw(self, draw:ImageDraw.ImageDraw):
        rotated = []
        for p in self.Polygons:
            p1 = Polygon(np.dot(p.Points, self.Rotation))
            rotated.append(p1)

        box = [
            self.Projection([-self.MaxX, self.MaxY, 0]),
            self.Projection([self.MaxX, self.MaxY, 0]),
            self.Projection([self.MaxX, -self.MaxY, 0]),
            self.Projection([-self.MaxX, -self.MaxY, 0]),
            self.Projection([-self.MaxX, self.MaxY, 0])
        ]
        draw.line(box, fill="#CCCCCCFF", width=1)
        rotated.sort(key=lambda k: - k.Depth)
        for p in rotated:
            draw.polygon(
                [
                    (p.Points[0,0] + 200, p.Points[0,2] + 350),
                    (p.Points[1,0] + 200, p.Points[1,2] + 350),
                    (p.Points[2,0] + 200, p.Points[2,2] + 350),
                    (p.Points[3,0] + 200, p.Points[3,2] + 350),
                ],
                fill   ='#cccccc00',
                outline='#ffffffff',
                width=1
            )



class IsometricImg:
    data:telemetry.NormalizedData
    BackGround : Image.Image
    Font: ImageFont.ImageFont
    TextOffset: float
    #Course
    Course: CourseData

    def __init__(self, data:telemetry.NormalizedData):
        self.TextOffset = 80
        self.data = data
        self.Course = CourseData(data=data)

        self.BackGround = Image.new('RGBA', (400, 400), '#00000000')
        draw = ImageDraw.Draw(self.BackGround)
        self.Font = ImageFont.truetype('/Users/tengdayan/Code/Gpx2Img/Tachyo-1.0.0.otf', size=50)
        textFont = ImageFont.truetype('Arial', size=30)
        draw.text([80,90 + self.TextOffset], 'km/h', fill='#EEEEEEFF', font=textFont)
        draw.text([295,90 + self.TextOffset], 'm', fill='#EEEEEEFF', font=textFont)

    def RenderFrame(self, filename, time:float):
        img = self.BackGround.copy()
        draw = ImageDraw.Draw(img)
        self.Course.SetRotationMatrix( -0.05 * time - np.pi / 6, np.pi / 8, 200)
        self.Course.Draw(draw)
        for i in range(0, len(self.data.DataPoints) - 1, 1):
            if self.data.DataPoints[i].TimeOffset <= time and self.data.DataPoints[i+1].TimeOffset > time :
                dpt = self.data.DataPoints[i]
                pt = self.Course.Projection([dpt.X, dpt.Y, dpt.Z])
                draw.ellipse(
                    [(pt[0] - 8,  pt[1] - 8), (pt[0] + 8, pt[1] + 8)], 
                    fill='#00FF00FF', 
                    width=6)
                draw.text([40,40 + self.TextOffset], '{:.1f}'.format(dpt.SPD), fill='#EEEEEEFF', font=self.Font, align='right')
                draw.text([250,40 + self.TextOffset], '{:.0f}'.format(dpt.ELE), fill='#EEEEEEFF', font=self.Font, align='right')
                break
        if(filename) :
            img.save(filename)
        else:
            img.show()
        
        
