#!/usr/bin/python

import time
import sys

print "STM32ON"
stmOnPin = 46

#export GPIO pin by opening file and writing the pin number to it
pinctl = open("/sys/class/gpio/export", "wb", 0)
try:
    pinctl.write( str(stmOnPin))
    print "Exported pin", str(stmOnPin)
except:
    print "Pin ", str(stmOnPin), " has been exported"
pinctl.close()

#set GPIO pin to be digital output
filename = '/sys/class/gpio/gpio%d/direction' % stmOnPin
pinctldir = open(filename, "wb", 0)
try:
    pinctldir.write("out")
    print "Set pin ", str(stmOnPin), " as digital output"
except:
    print "Failed to set pin direction"
pinctldir.close()

#unexport GPIO pin when we are done
def exit_gpio():
    pinctl = open("/sys/class/gpio/unexport", "wb", 0)
    try:
        pinctl.write( str(stmOnPin))
        print "Unexported pin", str(stmOnPin)
    except:
        print "Pin ", str(stmOnPin), " has been unexported"
    pinctl.close()

filename = '/sys/class/gpio/gpio%d/value' % stmOnPin
pin = open(filename, "wb", 0)
pin.write( str(1) )
