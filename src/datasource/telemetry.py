import datetime
from geopy.distance import geodesic 

class TelemetryDataPoint:
    Lat: float               # Latitude in degree 
    Lon: float               # Longitude in degree
    Ele: float               # Elevation in meters
    Time: datetime.datetime  # The timestamp
    
    def __init__(self, Time: datetime.datetime, Lat, Lon, Ele):
        self.Lat = Lat
        self.Lon = Lon
        self.Ele = Ele
        self.Time = Time

class NormalizedDataPoint:
    Time: datetime.datetime # The timestamp
    TimeOffset: float       # The offset from the beginning. in Seconds

    Xm: float # in meters, ease is positive
    Ym: float # in meters, north is positive
    Zm: float # in meters, up is positive
    
    X: float # in (-1,1), ease is positive
    Y: float # in (-1,1), north is positive
    Z: float # in (0,1), up is positive
    T: float # in seconds

    Delta: float # delta distance, in meters
    SPD: float # in km/h
    ELE: float # real elevation

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
                tdt.Z = dt.Z
                tdt.T = tdt.TimeOffset * coefT

                tdt.SPD = dt.SPD
                tdt.ELE = dt.ELE
                tdt.Delta = dt.Delta

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
    
    def Trim(self, start:float, length:float):
        datalist = []
        time0 = self.Datapoints[0].Time
        for dt in self.Datapoints:
            t = (dt.Time - time0).total_seconds()
            if t > start and t < start + length:
                datalist.append(dt)
        return TelemetryData(datalist)
    
    def Normalize(self, ZScale:float) -> NormalizedData:
        centerLat = (self.MaxLat + self.MinLat) / 2
        centerLon = (self.MaxLon + self.MinLon) / 2
        preLat = self.Datapoints[0].Lat
        preLon = self.Datapoints[0].Lon
        preT = 0

        normalized = NormalizedData()
        normalized.TotalSeconds = (self.MaxTime - self.MinTime).total_seconds()

        if self.MaxLon - self.MinLon > self.MaxLat - self.MinLat:
            coef = 2.0 / (self.MaxLon - self.MinLon)
        else:
            coef = 2.0 / (self.MaxLat - self.MinLat)

        coefT = 1.0 / normalized.TotalSeconds
        coefH = 1.0 / (self.maxEle - self.MinEle)

        for dt in self.Datapoints:
            ndp = NormalizedDataPoint()

            ndp.Time = dt.Time
            ndp.TimeOffset = (dt.Time - self.MinTime).total_seconds() 

            ndp.X = (dt.Lon - centerLon) * coef
            ndp.Y = (dt.Lat - centerLat) * coef
            ndp.Z = (dt.Ele - self.MinEle) * coefH * ZScale
            ndp.T = ndp.TimeOffset * coefT
            
            if dt.Lon >= centerLon :
                ndp.Xm = geodesic((centerLat, centerLon),(centerLat, dt.Lon)).meters 
            else:
                ndp.Xm = 0.0 - geodesic((centerLat, centerLon),(centerLat, dt.Lon)).meters 

            if dt.Lat >= centerLat :
                ndp.Xm = geodesic((centerLat, centerLon),(dt.Lat, centerLon)).meters
            else:
                ndp.Xm = 0.0 - geodesic((centerLat, centerLon),(dt.Lat, centerLon)).meters
            ndp.Zm = dt.Ele - self.MinEle

            ndp.ELE = dt.Ele

            ndp.Delta = geodesic((preLat, preLon),(dt.Lat, dt.Lon)).kilometers
            deltaT = ndp.TimeOffset - preT

            if deltaT == 0 :
                ndp.SPD = 0
            else:
                ndp.SPD = ndp.Delta / deltaT * 3600.0

            preLat = dt.Lat
            preLon = dt.Lon
            preT = ndp.TimeOffset

            normalized.DataPoints.append(ndp)

        return normalized



