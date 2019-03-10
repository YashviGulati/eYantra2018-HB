#!/usr/bin/env python2
import rospy
import roslib
from std_msgs.msg import Char,Int16

import sys, select, termios, tty

msg = """
Control Your Drone!
---------------------------
Moving around:
   u    i    o
   j    k    l
   n    m    ,


a : Arm drone
d : Dis-arm drone
r : stop smoothly
w : increase height
s : increase height

CTRL-C to quit
"""

"""
Function Name: getKey
Input: None
Output: keyboard charecter pressed
Logic: Determine the keyboard key pressed
Example call: getkey()
"""
def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
        sys.stdin.flush()
        #rospy.sleep(0.1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)
    rospy.init_node('simple_drone_teleop_key')
    pub = rospy.Publisher('/input_key',Int16, queue_size=1) #publish the key pressed
    rate=rospy.Rate(100)
    msg_pub=0
    keyboard_control={  #dictionary containing the key pressed abd value associated with it
                      'i': 10,
                      'k': 20,
                      'j': 30,
                      'l': 40,
                      'd':0, 
                      'w':50,
                      's':60,
                      'a':70,
                      'r':80,
                      't':90,
                      'p':100,
                      'm':110,
                      'n':120,
                      '+' : 15,
                      '1' : 1,#aruco
                      '2' : 2,#sal
                      '3' : 3,#mango
                      '4' : 4,#cashew
                      '5' : 5,#non food
                      '6' : 6,#Take out all trees from the arena
                      '7' : 7,#Disarm drone in the python code
                      '8' : 8}

    control_to_change_value=('u','o',',','z','c') #tuple containing the key that change the value

    try:
        pass
        # print value()
        while not rospy.is_shutdown():
          key = getKey()
          #print "asfdasdf"
          #print key
          if (key == '\x03'):
            break
          if key in keyboard_control.keys():
            msg_pub=keyboard_control[key]
            #print msg_pub
            pub.publish(msg_pub)
          if key in control_to_change_value:
            print "control_value"
            rate.sleep()
    except Exception as e:
        print e
    finally:
        print key
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
