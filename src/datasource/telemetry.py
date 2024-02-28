import datetime

class TelemetryDataPoint:
    Lat: float
    Lon: float
    Ele: float
    X: float
    Y: float
    Time: datetime.datetime
    
    def __init__(self, Time: datetime.datetime, Lat, Lon, Ele):
        self.Lat = Lat
        self.Lon = Lon
        self.Ele = Ele
        self.Time = Time

class NormalizedDataPoint:
    Time: datetime.datetime
    TimeOffset: float
    X: float
    Y: float
    E: float
    T: float

class NormalizedData:
    DataPoints: list[NormalizedDataPoint]
    TotalSeconds: float

    def __init__(self):
        self.DataPoints = []

    def Trim(self, start:float, length:float):
        trimmed = NormalizedData()
        trimmed.TotalSeconds = length
        coefT = 1.0 / length
        for dt in self.DataPoints:
            if dt.TimeOffset > start and dt.TimeOffset < start + length:
                tdt = NormalizedDataPoint()
                tdt.Time = dt.Time
                tdt.TimeOffset = dt.TimeOffset - start

                tdt.X = dt.X
                tdt.Y = dt.Y
                tdt.E = dt.E
                tdt.T = tdt.TimeOffset * coefT

                trimmed.DataPoints.append(tdt)
        return trimmed

class TelemetryData:
    def __init__(self, DataPoints : list[TelemetryDataPoint]):
        self.Datapoints = DataPoints
        minLat = DataPoints[0].Lat
        maxLat = DataPoints[0].Lat
        minLon = DataPoints[0].Lon
        maxLon = DataPoints[0].Lon
        minTime = DataPoints[0].Time
        maxTime = DataPoints[0].Time
        minEle = DataPoints[0].Ele
        maxEle = DataPoints[0].Ele


        for dt in self.Datapoints:
            if dt.Lat < minLat: minLat = dt.Lat
            if dt.Lat > maxLat: maxLat = dt.Lat
            if dt.Lon < minLon: minLon = dt.Lon
            if dt.Lon > maxLon: maxLon = dt.Lon
            if dt.Time > maxTime: maxTime = dt.Time
            if dt.Time < minTime: minTime = dt.Time
            if dt.Ele < minEle: minEle = dt.Ele
            if dt.Ele > maxEle: maxEle = dt.Ele
            
        self.MinLat = minLat
        self.MaxLat = maxLat
        self.MinLon = minLon
        self.MaxLon = maxLon
        self.MinTime = minTime
        self.MaxTime = maxTime
        self.MinEle = minEle
        self.maxEle = maxEle

    def Normalize(self) -> NormalizedData:
        normalized = NormalizedData()
        normalized.TotalSeconds = (self.MaxTime - self.MinTime).total_seconds()
        if self.MaxLon - self.MinLon > self.MaxLat - self.MinLat:
            coef = 1.0 / (self.MaxLon - self.MinLon)
        else:
            coef = 1.0 / (self.MaxLat - self.MinLat)

        coefT = 1.0 / normalized.TotalSeconds
        coefH = 1.0 / (self.maxEle - self.MinEle)

        for dt in self.Datapoints:
            ndp = NormalizedDataPoint()
            ndp.Time = dt.Time
            ndp.TimeOffset = (dt.Time - self.MinTime).total_seconds() 

            ndp.X = (dt.Lon - self.MinLon) * coef
            ndp.Y = 1 - (dt.Lat - self.MinLat) * coef
            ndp.T = ndp.TimeOffset * coefT
            ndp.E = (dt.Ele - self.MinEle) * coefH
            normalized.DataPoints.append(ndp)
        return normalized



