import sys
from time import sleep
import RPi.GPIO as GPIO
try:
    from ST_VL6180X import VL6180X
except ImportError:
    print("Error importing ST_VL6180X.VL6180X!")
    exit()

DISTANCE_QUEUE_SIZE = 10
PUSH_PULL_INTERVAL_CONSTANT = 60
ATTACHABLE_DISTANCE = 100
TOGGLE_INTERVAL_CONSTANT = 10
TOGGLE_INTERVAL = 5
TOF_READ_PERIOD = 0.005



def main():
    """-- Setup --"""
    debug = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "debug":  # sys.argv[0] is the filename
            debug = True

    # setup ToF ranging/ALS sensor
    tof_address = 0x29
    tof_sensor = VL6180X(address=tof_address, debug=debug)
    # apply pre calibrated offset
    tof_sensor.set_range_offset(23)
    print(f"Range offset set to: {tof_sensor.get_range_offset()}")
    # setup ToF ranging/ALS sensor
    tof_sensor.get_identification()
    if tof_sensor.idModel != 0xB4:
        print(f"Not a valid sensor id: {tof_sensor.idModel}")
    else:
        print(f"Sensor model: {tof_sensor.idModel}")
        print(f"Sensor model rev.: {tof_sensor.idModelRevMajor}.{tof_sensor.idModelRevMinor}")
        print(f"Sensor module rev.: {tof_sensor.idModuleRevMajor}.{tof_sensor.idModuleRevMinor}")
        print(f"Sensor date/time: {tof_sensor.idDate}/{tof_sensor.idTime}")
    tof_sensor.default_settings()
    sleep(1)

    """-- MAIN LOOP --"""
    mmDetectedDistance = 0
    frameList = []
    try:
        while True:
            mmDetectedDistance = tof_sensor.get_distance()
            # print(f"Measured distance is :{mmDetectedDistance} mm" )
            frameList.append(mmDetectedDistance)
            check_click(frameList)
            sleep(TOF_READ_PERIOD)
    except KeyboardInterrupt:
        print("\nquit")


def check_click(distanceList : list):
    if(len(distanceList) >= DISTANCE_QUEUE_SIZE):
        maxDistance = max(distanceList)
        minDistance = min(distanceList)
        intervalDistance = maxDistance - minDistance
        maxIndex = distanceList.index(maxDistance)
        minIndex = distanceList.index(minDistance)
        indexInterval = maxIndex - minIndex
        if(intervalDistance > PUSH_PULL_INTERVAL_CONSTANT):
            if( maxIndex > minIndex):
                ## Rising edge
                pull()
            else:
                ## falling edge
                push()
            distanceList.clear()
        elif(maxDistance < ATTACHABLE_DISTANCE):
            if(intervalDistance > TOGGLE_INTERVAL_CONSTANT):
                toggle()
            # toggle()
                distanceList.clear()
            distanceList.pop()

def push():
    # buzzer()
    print("push")

def pull():
    print("pull")

def toggle():
    print("toggle")

if __name__== "__main__":
    main()