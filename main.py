# Super simplistic weight transmitter simulator
# TODO: stable/unstable, etc

import serial
ser = serial.Serial("COM5", 9600, timeout=0)
from time import sleep

import sys
import threading
import time
import queue

def add_input(input_queue):
    while True:
        input_queue.put(sys.stdin.read(1))

input_queue = queue.Queue()

input_thread = threading.Thread(target=add_input, args=(input_queue,))
input_thread.daemon = True
input_thread.start()

last_update = time.time()

msg=[]
want_weight = int(sys.argv[1] or 0)
while True:
	sleep(0.01)
	
	ser.flushInput()
	b = ser.inWaiting()
	if b>0:
		print(ser.read(b), end='')
	now = time.time()
	if now-last_update>0.05:
		last_update = now
		ser.write(b"ST,GS,   %5s, g\r\n"%(b"%d"%(want_weight,)))

	if not input_queue.empty():
		char = input_queue.get()
		if char == "\r" or char == "\n":
			command = "".join(msg)
			msg=[]
			if command!="":
				print("Transmit weight:",command)
				want_weight = int(command)
		else:
			msg.append(char)
		
