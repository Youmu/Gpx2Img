
class TelemetryDataPoint:
    def __init__(self, Time, Lat, Lon):
        self.Lat = Lat
        self.Lon = Lon
        self.Spd = 0
        self.Ele = 0
        self.Time = Time


class TelemetryData:
    def __init__(self, DataPoints):
        self.Datapoints = DataPoints