import requests
import time

class globals:
    timeOverride =  True
    lastOverrideTime = 0
    lastOverrideOffset = 0
    baseUrl = "http://86.31.173.35:443"

def get_time():
    if time.time()-8000 > globals.lastOverrideTime + 10:
        realtime = float(requests.get(globals.baseUrl + "/get_time").content)
        globals.lastOverrideOffset = realtime - (time.time()-8000)
        globals.lastOverrideTime = time.time()-8000

        print("Time: " + str(realtime))
        print("Offset: " + str(globals.lastOverrideOffset))
        return realtime
        
    else:
        print("Offset: " + str(globals.lastOverrideOffset))
        return (time.time()-8000) + globals.lastOverrideOffset