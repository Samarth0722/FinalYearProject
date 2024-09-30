# import serial
# import time
# import string
# import pynmea2
# from pubnub.pnconfiguration import PNConfiguration
# from pubnub.pubnub import PubNub
# from pubnub.exceptions import PubNubException

# pnChannel = "raspi-tracker";

# pnconfig = PNConfiguration()
# pnconfig.subscribe_key = "Your Subscribe key"
# pnconfig.publish_key = "Your Publish key"
# pnconfig.ssl = False
 
# pubnub = PubNub(pnconfig)
# pubnub.subscribe().channels(pnChannel).execute()



import math
import numpy as np


geofencePoints = [
    {
        'lat': 13.1316,
        'lng': 77.5907,
        'circularRightDist': 0
      },
      {
        'lat': 13.1299,
        'lng': 77.6019,
        'circularRightDist': 0
      },
      {
        'lat': 13.1206,
        'lng': 77.6091,
        'circularRightDist': 0
      },
      {
        'lat': 13.1142,
        'lng': 77.5961,
        'circularRightDist': 0
      },
      {
        'lat': 13.1308,
        'lng': 77.5820,
        'circularRightDist': 0
      },

]


def haversine_dist(c1, c2):
    R = 6371.0710
    rlat1 = math.radians(c1.lat)
    rlat2 = math.radians(c2.lat)
    difflat = rlat2-rlat1
    difflon = math.radians(c2.lng - c1.lng)
    d = 2 * R * np.arcsin(math.sqrt(math.sin(difflat/2) * math.sin(difflat/2) + math.cos(rlat1) * math.cos(rlat2) * math.sin(difflon/2) * math.sin(difflon/2)))
    return d

print(haversine_dist(geofencePoints[0], geofencePoints[1]))
# print(geofencePoints)

for i in range(0, geofencePoints.length):
    geofencePoints[i]['circularRightDist'] = haversine_dist(geofencePoints[i], geofencePoints[(i+1) % geofencePoints.length])

for e in geofencePoints:
    print(e)


def radians_to_degrees(radians):
    pi = math.pi
    return radians * (180/pi)

def getAngle(b, c, a):
    numerator = (b * b) + (c * c) - (a * a)
    denominator = 2 * b * c

    return radians_to_degrees(math.acos(numerator/denominator))

def isInside(coordinate):
    firstDist = haversine_dist(coordinate, geofencePoints[0])
    dist1 = firstDist
    dist2 = 1
    andgleSum = 0

    for i in range(0, len(geofencePoints)):
        dist2 = haversine_dist(coordinate, geofencePoints[(i+1) % len(geofencePoints)])
        angle = getAngle(dist1, dist2, geofencePoints[i]['circularRightDist'])

        angleSum += angle
        dist1 = dist2

    return angleSum > 355.0

# print(isInside({'lat': 13.1307, 'lng': 77.5900}))
# while True:
#     port="/dev/ttyAMA0"
#     ser=serial.Serial(port, baudrate=9600, timeout=0.5)
#     dataout = pynmea2.NMEAStreamReader()
#     newdata=ser.readline()

#     if newdata[0:6] == "$GPGLL":
#         newmsg=pynmea2.parse(newdata)
#         lat=newmsg.latitude
#         lng=newmsg.longitude
#         try:
#             envelope = pubnub.publish().channel(pnChannel).message({
#             'lat':lat,
#             'lng':lng
#             }).sync()
#             print("publish timetoken: %d" % envelope.result.timetoken)
#         except PubNubException as e:
#             handle_exception(e)