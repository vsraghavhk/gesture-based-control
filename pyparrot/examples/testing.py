"""
Demo the trick flying for the python interface

Author: Amy McGovern
"""

from pyparrot.Anafi import Anafi

# you will need to change this to the address of YOUR anafi
mamboAddr = "e0:14:d0:63:3d:d0"

# make my anafi object
# remember to set True/False for the wifi depending on if you are using the wifi or the BLE to connect
anafi = Anafi(mamboAddr, use_wifi=True)

print("trying to connect")
success = anafi.connect(num_retries=3)
print("connected: %s" % success)

if (success):
    # get the state information
    print("sleeping")
    anafi.smart_sleep(2)
    anafi.ask_for_state_update()
    anafi.smart_sleep(2)

    print("taking off!")
    anafi.safe_takeoff(5)

    if (anafi.sensors.flying_state != "emergency"):
        print("flying state is %s" % anafi.sensors.flying_state)
        print("Flying direct: going up")
        anafi.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=20, duration=1)

        print("flip left")
        print("flying state is %s" % anafi.sensors.flying_state)
        success = anafi.flip(direction="left")
        print("anafi flip result %s" % success)
        anafi.smart_sleep(5)

        print("flip right")
        print("flying state is %s" % anafi.sensors.flying_state)
        success = anafi.flip(direction="right")
        print("anafi flip result %s" % success)
        anafi.smart_sleep(5)

        print("flip front")
        print("flying state is %s" % anafi.sensors.flying_state)
        success = anafi.flip(direction="front")
        print("anafi flip result %s" % success)
        anafi.smart_sleep(5)

        print("flip back")
        print("flying state is %s" % anafi.sensors.flying_state)
        success = anafi.flip(direction="back")
        print("anafi flip result %s" % success)
        anafi.smart_sleep(5)

        print("landing")
        print("flying state is %s" % anafi.sensors.flying_state)
        anafi.safe_land(5)
        anafi.smart_sleep(5)

    print("disconnect")
    anafi.disconnect()