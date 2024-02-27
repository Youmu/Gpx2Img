import datetime

class TelemetryDataPoint:
    Lat: float
    Lon: float
    Ele: float
    Time: datetime.datetime
    
    def __init__(self, Time : datetime.datetime, Lat, Lon, Ele):
        self.Lat = Lat
        self.Lon = Lon
        self.Ele = Ele
        self.Time = Time


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