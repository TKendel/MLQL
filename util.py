import gpxpy

def parsegpx(path):
    points = list()
    with open(path,'r') as gpxfile:
        gpx = gpxpy.parse(gpxfile)
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    dict = {'Timestamp': point.time,
                            'Latitude': point.latitude,
                            'Longitude': point.longitude,
                            'Elevation': point.elevation,
                            'Speed': float(point.extensions[0].text),
                            'Course': float(point.extensions[1].text),
                            'hAcc': float(point.extensions[2].text),
                            'vAcc': float(point.extensions[3].text),
                            }
                    points.append(dict)
    return points
