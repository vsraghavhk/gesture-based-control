import Leap, sys, thread, time, math, re
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

filename = "D:\Documents\TAMU\Course Work\Fall 2020\CSCE 685 - Directed Studies - Dr. Murphy\commands.txt"

command_delay = 0.5 # seconds

# Defaults.
status = "on_ground" 

command_timer = 0
command_to_write = None

ack = False
ack_wait = False
prev_command = command_to_write
i = 0

class leapMotionListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    # methods
    def on_init(self, controller):
        print "Listener initialized."

    def on_connect(self, controller):
        print "Motion Sensor connected."

        # Gestures must have semicolons;
        # WHY?
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        print "Motion Sensor disconnected!"

    def on_exit(self, controller):
        print "Exiting..."

    def reset_all(self):
        global ack, ack_wait, prev_command, i
        global command_timer, command_to_write

        i=0
        command_timer = 0
        command_to_write = None
        prev_command = command_to_write
        ack_wait = False
        ack = False

        # print "Everything has been reset."

    def execute(self, command_to_write):
        with open(filename, 'w+') as new:
            new.write(command_to_write)
        print "\"" + command_to_write + "\" command sent to drone.\n"
        print "Sensor paused for execution.\n"
        time.sleep(2)
        print "Sensor waiting for command.\n"

    def thumb_command(self, ext_fingers):
        global status, prev_command, ack, ack_wait, command_timer

        the_command = None
        if len(ext_fingers)==1 and ext_fingers[0].type==0:
            # Only Thumb is extended.
            finger = ext_fingers[0]
            
            if finger.direction.z > 0: # and status == "on_ground":
                # Fly Command from ground.
                the_command = "fly"
                
            elif finger.direction.z < 0: # and status == "on_air":
                # Land command from ground.
                the_command = "land"

        if the_command != None:
            # IF there is a pending comment, 
            # Check if there is an acknowledgement waiting 
            # check if it can be acknowledged.
            if ack_wait == True:
                if (time.time()-command_timer >= 2):
                    if prev_command==command_to_write:
                        ack = True
                    else:
                        print "Command rescinded. \n"
                        self.reset_all()

        return the_command
    
    def on_frame(self, controller):
        # 290 frames per second.
        global ack, ack_wait, prev_command, i
        global status, command_timer, command_to_write, command_delay

        # Timestamp in microseconds!
        frame = controller.frame()

        # If more than 1 hand is in view,
        if len(frame.hands)>1:
            print "There is more than 1 hand on frame! Please only use 1 hand. "
            self.reset_all
            print "Pausing for 2 seconds..."    
            time.sleep(2)
            print "\n"
        
        # If only 1 hand is in view,
        else: 
            # This means only one hand is considered in every frame. 
            hand = frame.hands[0]
            # handType = "Left Hand" if hand.is_left else "Right Hand"
            # normal = hand.palm_normal
            
            gesture = frame.gestures()[0]
            ext_fingers = hand.fingers.extended()
            
            # Commands for when drone is on ground.
            #if status == "on_ground":
            command_to_write = self.thumb_command(ext_fingers)

            if command_timer==0 and command_to_write != None:
                command_timer = time.time()
                # print "command timer has been set."
            
            # Commands for when drone is in air.
            #elif status == "on_air":
            # if swipe, turn accordingly
            if gesture.type == Leap.Gesture.TYPE_SWIPE: 
                swipe = SwipeGesture(gesture)
                
                # print str(swipe.state)
                
                if swipe.state < 3:
                    self.reset_all()

                else: 
                    command_timer = time.time()
                    swipe_dir = swipe.direction

                    if swipe_dir.x>0 and math.fabs(swipe_dir.x) > math.fabs(swipe_dir.y): # and math.fabs(swipe_dir.x) > math.fabs(swipe_dir.z):
                        print "Right Swipe"
                        command_to_write = "turn left"
                        # Add turn left command

                    elif swipe_dir.x<0 and math.fabs(swipe_dir.x) > math.fabs(swipe_dir.y): # and math.fabs(swipe_dir.x) > math.fabs(swipe_dir.z):
                        print "Left Swipe"
                        command_to_write = "turn right"
                        # Add turn right command
                    
                    '''
                        elif swipe_dir.z>0 and math.fabs(swipe_dir.z) > math.fabs(swipe_dir.x): # and math.fabs(swipe_dir.z) > math.fabs(swipe_dir.y):
                            print "Up Swipe"

                        elif swipe_dir.z<0 and math.fabs(swipe_dir.z) > math.fabs(swipe_dir.x): # and math.fabs(swipe_dir.z) > math.fabs(swipe_dir.y):
                            print "Down Swipe"
                        
                        elif swipe_dir.y>0 and math.fabs(swipe_dir.y) > math.fabs(swipe_dir.x): # and math.fabs(swipe_dir.y) > math.fabs(swipe_dir.z):
                            print "Forward Swipe"

                        elif swipe_dir.y<0 and math.fabs(swipe_dir.y) > math.fabs(swipe_dir.x): # and math.fabs(swipe_dir.y) > math.fabs(swipe_dir.z):
                            print "Backward Swipe"
                    '''
                        
            # if not swipe, is it land command?
            else:
                command_to_write = self.thumb_command(ext_fingers)

                if command_timer==0 and command_to_write != None:
                    command_timer = time.time()
                    print "command timer has been set."

            # Analyse command to execute or wait
            if command_to_write != None :
                if command_to_write=="turn left" or command_to_write=="turn right":
                    # write swipe command.
                    # and (time.time()-command_timer > command_delay)
                    time.sleep(command_delay)
                    self.execute(command_to_write)
                    print "Turning Complete. (" + status + ") \n"

                    self.reset_all()
                
                elif command_to_write == "fly" or command_to_write == "land":
                    if (time.time()-command_timer >= 2): # after 2 seconds
                        # Write fly/land command.
                        # Are you waiting for ack?
                        
                        if ack_wait == True: # Yes. Check for ack.
                            if ack == True : # If ack and same command, then execute.
                                self.execute(command_to_write)
                                if command_to_write=="fly" and status=="on_ground":
                                    status = "on_air"
                                elif command_to_write=="land" and status=="on_air":
                                    status = "on_ground"
                                else:
                                    print "Redundant command? The drone should be " + status + ". \n"
                                
                                self.reset_all()

                            elif ack == False: #If no ack or different command, reset.
                                print "Command not registered. Please hold command for 2 seconds.\n"
                                self.reset_all()

                        elif ack_wait == False: # No. Set wait for ack and prev_command received.
                            prev_command = command_to_write
                            ack_wait = True
                            ack = False
                        
                        else: # unlikely scenario. Present for fallback.
                            print "!!! There seems to be some error here. !!!\n" 
                            self.reset_all()
                
                    else:
                        if i==0:
                            print "Hold. Reading command...\n"
                            i = 1
                else:
                    print "!!! Unknown Command! Will be ignored. !!!\n"
                    self.reset_all()
            else:
                # No command
                pass


def main():
    listener = leapMotionListener()
    controller = Leap.Controller()
    controller.add_listener(listener)
    print "Press Enter to quit..."

    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass 
    finally:
        controller.remove_listener(listener)
    
if __name__ == '__main__':
    main()
        