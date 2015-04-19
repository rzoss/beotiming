import urllib.request
import time

def check_connectivity(reference):
    try:
        urllib.request.urlopen(reference, timeout=1)
        return True
    except urllib.request.URLError:
        return False


if __name__ == "__main__":
    print("Startup beo-timing.ch")
    # test internet connection
    print("check connection")
    i = 0
    while not check_connectivity('http://www.beo-timing.ch'):
        # retry every second
        print("conn. failed")
        i += 1
        print("retry #" + str(i))
        time.sleep(1)
    print('Connection test successfull. Startup finished.')