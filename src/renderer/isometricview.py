from PIL import Image, ImageColor, ImageDraw, ImageFont
import math
import numpy as np
from datasource import telemetry

class CourseData:
    Course: np.matrix
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
        self.Shadow = self.Course.copy()
        self.Shadow[:,2] = 0

    def SetRotationMatrix(self, alpha, beta):
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
        self.Rotation = np.dot(rot1, rot2)
        return self.Rotation
    
    def Projection(self, point):
        p = np.dot(point, self.Rotation)
        return (p[0,0] * 200 + 200, p[0,2] * (-200) + 350)

    def Draw(self, draw:ImageDraw.ImageDraw):
        lcourse = np.dot(self.Course, self.Rotation)
        lcourseProj = lcourse[:,[0,2]] * [[200,0],[0, -200]] + [200, 350]
        lshadow = np.dot(self.Shadow, self.Rotation)
        lshadowProj = lshadow[:,[0,2]]  * [[200,0],[0, -200]] + [200, 350]
        dt1 = []
        dt2 = []
        for i in range(0, self.Rows):
            pt1 = (lcourseProj[i, 0], lcourseProj[i, 1])
            pt2 = (lshadowProj[i, 0], lshadowProj[i, 1])
            dt1.append(pt1)
            dt2.append(pt2)
            draw.line([pt1, pt2], fill="#CCCCCCFF", width=1)
        draw.line(dt1, fill="#CCCCCCFF", width=3)
        draw.line(dt2, fill="#CCCCCCFF", width=3)
        box = [
            self.Projection([-self.MaxX, self.MaxY, 0]),
            self.Projection([self.MaxX, self.MaxY, 0]),
            self.Projection([self.MaxX, -self.MaxY, 0]),
            self.Projection([-self.MaxX, -self.MaxY, 0]),
            self.Projection([-self.MaxX, self.MaxY, 0])
        ]
        draw.line(box, fill="#CCCCCCFF", width=1)


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

    def RenderPreview(self, filename):
        img = self.BackGround.copy()
        draw = ImageDraw.Draw(img)
        self.Course.SetRotationMatrix(0.0 - np.pi / 6, np.pi / 8)
        self.Course.Draw(draw)
        self.BackGround.save(filename)


    def RenderFrame(self, path, nameprefix, time:float, nframe:int):
        img = self.BackGround.copy()
        draw = ImageDraw.Draw(img)
        self.Course.SetRotationMatrix( -0.05 * time - np.pi / 6, np.pi / 8)
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
        path = '{p}/{prefix}{nb:05d}.png'.format(p=path, prefix=nameprefix, nb=nframe)
        img.save(path)
        
        
