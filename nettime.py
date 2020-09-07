import requests
import time

class globals:
    timeOverride = False
    lastOverrideTime = 0
    lastOverrideOffset = 0
    baseUrl = "http://86.31.173.35:443"

def get_time():
    if time.time() > globals.lastOverrideTime + 30:
        realtime = float(requests.get(globals.baseUrl + "/get_time").content)
        globals.lastOverrideOffset = realtime - time.time()
        globals.lastOverrideTime = time.time()

        print("Time: " + str(realtime))
        return realtime
        
    else:
        return time.time() + globals.lastOverrideOffset