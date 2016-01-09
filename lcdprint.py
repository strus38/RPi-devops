import sys, signal, socket
import serial, time

## Add it to a crontab entry if you need it to run regularly
## crontab -e
## add this line at the bottom:
## 00 * * * * python /root/lcdprint.py 

print "Welcome in RPi LCD Monitor"
ser = serial.Serial()

def run_prg():

    #initialization and open the port
    #possible timeout values:
    #    1. None: wait forever, block call
    #    2. 0: non-blocking mode, return immediately
    #    3. x, x is bigger than 0, float allowed, timeout block call
    ser.port = "/dev/ttyUSB0"
    ser.baudrate = 115200
    ser.bytesize = serial.EIGHTBITS #number of bits per bytes
    ser.parity = serial.PARITY_NONE #set parity check: no parity
    ser.stopbits = serial.STOPBITS_ONE #number of stop bits
    ser.timeout = 0       #non-block read
    ser.xonxoff = False   #disable software flow control
    ser.rtscts = True    #disable hardware (RTS/CTS) flow control
    time.sleep(.5)
    ser.rtscts = False    #disable hardware (RTS/CTS) flow control
    ser.dsrdtr = False    #disable hardware (DSR/DTR) flow control
    ser.writeTimeout = 2  #timeout for write

    ip=[(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]

    try: 
        ser.open()
    except Exception, e:
        print "error open serial port: " + str(e)
        exit()

    if ser.isOpen():
        try:
            iter = 0
            while iter < 3:
    	        ip=[(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
                #ser.flushInput() #flush input buffer, discarding all its contents
                #ser.flushOutput()#flush output buffer, aborting current output 
                ser.write(ip)
                print("write data: "+str(ip))
                time.sleep(5)  #give the serial port sometime to receive the data
		iter = iter+1
            
            # Need to find a way to read from serial the keyshield interruptions... to write the message corresponding to the pressed key.
            
            ser.close() # Useless
            exit()
        except Exception, e1:
            print "error communicating...: " + str(e1)

    else:
        print "cannot open serial port "

def exit_gracefully(signum, frame):
    # restore the original signal handler as otherwise evil things will happen
    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
    signal.signal(signal.SIGINT, original_sigint)

    try:
        if raw_input("\nReally quit? (y/n)> ").lower().startswith('y'):
            if ser.isOpen():
                ser.close()
            sys.exit(1)

    except KeyboardInterrupt:
        print("Ok ok, quitting")
        sys.exit(1)

    # restore the exit gracefully handler here    
    signal.signal(signal.SIGINT, exit_gracefully)

if __name__ == '__main__':
    # store the original SIGINT handler
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)
    run_prg()
