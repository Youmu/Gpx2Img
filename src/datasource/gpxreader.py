import xml.etree.ElementTree as ET
import datetime
from datasource import telemetry

ns = {"gpx": "http://www.topografix.com/GPX/1/1"}

class gpxreader:
    def LoadGpx(self, filename):
        tree = ET.parse(filename)
        gpxroot = tree.getroot()
        trk = gpxroot.find(path='gpx:trk/gpx:name', namespaces=ns)
        trkseg = gpxroot.find(path='gpx:trk/gpx:trkseg', namespaces=ns)
        count = 0
        datapts = []
        for c in trkseg.findall("gpx:trkpt", ns):
            count = count + 1
            lat = float(c.get('lat'))
            lon = float(c.get('lon'))
            timeStr = c.find(path='gpx:time', namespaces=ns).text
            time = datetime.datetime.fromisoformat(timeStr)
            ele = float(c.find(path='gpx:ele', namespaces=ns).text)
            datapts.append(telemetry.TelemetryDataPoint(time, lat, lon, ele))
        print(count)
        return telemetry.TelemetryData(datapts)