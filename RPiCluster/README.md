# Arduino code to display RPi info on a LCD

This code must run on an arduino connected to a LCD.
I used this method because that what I had in my garage...

The Arduino and the RPi are communicating using USB port (USB0 by default).

Just connect the USB port to any RPi to get its public IP.
The IP is retrieved using a connection to Google... not using ````$ ip addr``` command.
