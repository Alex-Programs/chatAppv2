import requests
import time

class globals:
    timeOverride =  True
    lastOverrideTime = 0
    lastOverrideOffset = 0
    baseUrl = "http://86.31.173.35:443"


def faketime():
    return time.time()

def get_time():
    if faketime() > globals.lastOverrideTime + 10:
        realtime = float(requests.get(globals.baseUrl + "/get_time").content)
        globals.lastOverrideOffset = realtime - (faketime())
        globals.lastOverrideTime = faketime()

        print("Time: " + str(realtime))
        print("Offset: " + str(globals.lastOverrideOffset))
        return realtime
        
    else:
        return (faketime()) + globals.lastOverrideOffset