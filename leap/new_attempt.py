import Leap, sys, thread, time, math, re
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

filename = "D:\Documents\TAMU\Course Work\Fall 2020\CSCE 685 - Directed Studies - Dr. Murphy\commands.txt"


class leapMotionListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    # methods
    def on_init(self, controller):
        self.hold_time = 2
        self.swipe_thresh = 4

        self.status = "on_ground"
        self.swipe_count = 0
        self.gesture_time = None 
        self.last_command = None
        self.command_to_write = None
        self.frame_count = 0
        self.last_frame_number = 0

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
        self.swipe_count = 0
        self.gesture_time = None 
        self.last_command = None
        self.command_to_write = None

    def execute(self):
        global filename
        with open(filename, 'w+') as new:
            new.write(self.command_to_write)
        print "\"" + self.command_to_write + "\" command sent to drone.\n"
        print "Sensor paused for execution.\n"
        time.sleep(2)
        print "Sensor waiting for command.\n"

    def record_frame(self):
        if self.command_to_write != self.last_command:
            self.reset_all()
        else:
            if self.command_to_write == "fly" or self.command_to_write == "land":
                if time.time() - self.gesture_time > self.hold_time:
                    self.execute()


            elif self.command_to_write == "turn left" or self.command_to_write == "turn right" :
                self.swipe_count = self.swipe_count + 1

                if self.swipe_count == self.swipe_thresh:
                    self.execute()
        
        self.last_command = self.command_to_write

        print self.last_command

                
    def on_frame(self, controller):
        # 290 frames per second.

        # Timestamp in microseconds!
        frame = controller.frame()

        # If more than 1 hand is in view,
        if len(frame.hands) > 1:
            print "There is more than 1 hand on frame! Please only use 1 hand. "
            self.reset_all
            print "Pausing for 2 seconds..."    
            time.sleep(2)
            print "\n"
        
        # If only 1 hand is in view,
        else: 
            self.command_to_write = None 
            
            # This means only one hand is considered in every frame. 
            hand = frame.hands[0]
            
            # Get and store gestures and fingers.
            gesture = frame.gestures()[0]
            ext_fingers = hand.fingers.extended()
            
            # Look for thumbs up/down.
            if len(ext_fingers)==1 and ext_fingers[0].type==0:
                finger = ext_fingers[0]
                
                if finger.direction.z>0:
                    self.command_to_write = "fly"
                    if self.gesture_time == None:
                        self.gesture_time = time.time()
                elif finger.direction.z<0:
                    self.command_to_write = "land"
                    if self.gesture_time == None:
                        self.gesture_time = time.time()

                 
            # Look for swipe gestures. 
            elif gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)
                
                swipe_dir = swipe.direction
                if swipe_dir.x>0 and math.fabs(swipe_dir.x) > math.fabs(swipe_dir.y): # and math.fabs(swipe_dir.x) > math.fabs(swipe_dir.z):
                    # print "Right Swipe"
                    self.command_to_write = "turn left" 
                    # Add turn left command

                elif swipe_dir.x<0 and math.fabs(swipe_dir.x) > math.fabs(swipe_dir.y): # and math.fabs(swipe_dir.x) > math.fabs(swipe_dir.z):
                    # print "Left Swipe"
                    self.command_to_write = "turn right"
                    # Add turn right command
            
            # If no gestures are found.
            else:
                self.reset_all()

        self.record_frame() 
        


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
        