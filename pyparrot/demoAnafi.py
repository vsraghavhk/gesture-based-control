import os
import time
import numpy as np
from pyparrot.Anafi import Anafi
#from pyparrot.DroneVisionGUI import DroneVisionGUI
from pyparrot.DroneVision import DroneVision
from pyparrot.Model import Model

filename = "D:\Documents\TAMU\Course Work\Fall 2020\CSCE 685 - Directed Studies - Dr. Murphy\commands.txt"
#filename = "/Users/lesliekim/Documents/DEV/pyparrot/commands.txt"
debug_mode = True

class UserVision:
    def __init__(self, vision):
        self.index = 0
        self.vision = vision

    def save_pictures(self, args):
        img = self.vision.get_latest_valid_picture()
        if img is not None and WRITE_IMAGES:
            #cv2.imwrite(f"image_{self.index:06d}.png", img)
            cv2.imwrite("image_{}.png".format(img))
            self.index += 1

def demo_anafi_user_vision(anafi_vision, args):
    """
    Demo the user code to run with the run button for a mambo

    :param args:
    :return:
    """
    anafi = args[0]

    print("Sleeping for 15 seconds, move Anafi around to test vision")
    anafi.smart_sleep(15)
    anafi.start_video_stream()

    print("Closing video stream")
    anafi.close_video()

    anafi.smart_sleep(5)

    print("Disconnecting Anafi")
    anafi.disconnect()


def main():

    print("connecting")
    if not debug_mode:
        anafi = Anafi(drone_type="Anafi", ip_address="192.168.42.1")
        success = anafi.connect(10)
    elif debug_mode:
        success = True


    if (success):
        if not debug_mode:
            anafi.ask_for_state_update()
            print(anafi.sensors.flying_state)

        '''
                #vision
                print("Starting vision")
                anafi_vision = DroneVision(anafi, Model.ANAFI)
                user_vision = UserVision(anafi_vision)
                anafi_vision.set_user_callback_function(
                    user_vision.save_pictures, user_callback_args=None
                )
        
            #video
                if anafi_vision.open_video():
                    print("Opened video feed")
                    print("Sleeping for 15 seconds - move Anafi around to test feed")
                    anafi.smart_sleep(15)
                    print("Closing video feed")
                    anafi_vision.close_video()
                    anafi.smart_sleep(5)
                else:
                    print("Could not open video feed")
        
        '''
        '''
        print("Preparing to open video stream")
        anafi_vision = DroneVisionGUI(
            anafi,
            Model.ANAFI,
            buffer_size=200,
            user_code_to_run=demo_anafi_user_vision,
            user_args=(anafi,),
        )
        user_vision = UserVision(anafi_vision)
        anafi_vision.set_user_callback_function(
            user_vision.save_pictures, user_callback_args=None
        )

        print("Opening video stream")
        anafi_vision.open_video()

        anafi.smart_sleep(10)
        '''

        command_flag = 1
        fly_flag = 0
        land_flag = 0
        right_flag = 0
        left_flag = 0
        drone_status = 0 # 0 : on the ground ; 1 : in the air

        while command_flag == 1:
            with open(filename, "r+") as new:
                command = new.readline().lower()
                if command == "fly":
                    fly_flag = 1
                    new.truncate(0)
                    new.close()

                elif command == "land":
                    land_flag = 1
                    new.truncate(0)
                    new.close()

                elif command == "turn right":
                    right_flag = 1
                    new.truncate(0)
                    new.close()

                elif command == "turn left":
                    left_flag = 1
                    new.truncate(0)
                    new.close()

                else:
                    print("No new commands")

            # take-off when 'takeoff' & drone is on the ground
            if fly_flag == 1 and drone_status == 0:
                print("Take off")
                if not debug_mode:
                    anafi.safe_takeoff(5)
                drone_status = 1
                fly_flag = 0

            # land when 'land' & drone is in the air
            if land_flag == 1 and drone_status == 1:
                print("Land")
                if not debug_mode:
                    anafi.safe_land(5)
                land_flag = 0
                drone_status = 0
                command_flag = 0

            # turn when 'turn right" & drone is in the air
            if right_flag == 1 and drone_status == 1:
                print("Turn Right 30 degree")
                if not debug_mode:
                    anafi.move_relative(dx=0, dy=0, dz=0, dradians=np.pi / 6)
                right_flag = 0

            #turn when 'turn left" & drone is in the air
            if left_flag == 1 and drone_status == 1:
                print ("Turn Left 30 degree")
                if not debug_mode:
                    anafi.move_relative(dx=0, dy=0, dz=0, dradians=-np.pi / 6)
                left_flag = 0


            time.sleep(1)

        print("DONE - disconnecting")
        if not debug_mode:
            anafi.disconnect()
    else:
        print("Error connecting Anafi")

if __name__ == "__main__":
    main()


