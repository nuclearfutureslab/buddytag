#!/usr/bin/python

import sys
import time
import serial
import signal


ser = serial.Serial(port="/dev/ttyAMA0", baudrate = 230400, timeout=None)
ser.close()
ser.open()

dglen = 38      # See STIM Datasheet: http://www.sensonor.com/media/84604/2015-08-25-product-brief-stim300-a4.pdf

datarate = 500  # STIM samples per sec
dt = 1.0/datarate

# Exit cleanly on SIGINT. See https://docs.python.org/2/library/signal.html
def signal_handler(signum, frame):
    exit()

signal.signal(signal.SIGINT, signal_handler)

def getAcc(acc1,acc2,acc3):
    #  Numerator of formula from pg 42 of STIM datasheet  
    acc = (int(acc1)*65536 + int(acc2)*256 + int(acc3))  
    #  Test to see if two's complement of numerator is neccessary 
    if acc >= 8388608:         # if acc is bigger than 2**24 (acc is 24 bit number)                  
        #  Convert to negative signed integer
        acc = (acc - 16777216)   # subtract 2**23 to get 2's compliment of acc
    return acc/524288.0 

def ser_init():
    raw = ser.read(dglen+1)
    if (ord(raw[0]) == 147 and ord(raw[dglen]) == 147):
        # print "initialized"
        return True
    else:
        return False

def getdata():
    raw = ser.read(dglen)
    data = [ord(i) for i in raw]
    
    ax = getAcc(data[11], data[12], data[13])
    ay = getAcc(data[14], data[15], data[16])
    az = getAcc(data[17], data[18], data[19])
    accs = str(ax)+'\t'+str(ay)+'\t'+str(az)
    return accs


def main():


    start_time = time.time()
    
    initializing = True
    
    while initializing:
        initialized = ser_init()
        if initialized:
            break
    ser.read(dglen-1)
    
    running = True

    while running:
        sys.stdout.write(str(time.time() - start_time))
        sys.stdout.write("\t")
        sys.stdout.write(getdata())

        sys.stdout.write("\n")

if __name__ == "__main__":
    main()
    
    
    
    
## THE END