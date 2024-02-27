import xml.etree.ElementTree as ET
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
            datapts.append(telemetry.TelemetryDataPoint(0,lat, lon))

        print(count)
        return telemetry.TelemetryData(datapts)