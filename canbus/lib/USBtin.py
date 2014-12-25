#!/usr/bin/python
# -* coding: utf-8 *-

import time
import serial
import os, sys


class USBtin(object):
  ser = None
  hw_ver = None
  fw_ver = None

  def __init__(self, port):
	# configure the serial connections (the parameters differs on the device you are connecting to)
	self.ser = serial.Serial(
	    port='/dev/ttyACM0',
	    baudrate=19200,
	    parity=serial.PARITY_NONE,
	    stopbits=serial.STOPBITS_ONE,
	    bytesize=serial.EIGHTBITS,
	    timeout=1
	)
	

	self.ser.open()
	if not self.ser.isOpen():
	  print 'Fehler!'
	
	# clear state, close connection
	self.ser.write("\rC\r")
	time.sleep(0.1)
	self.ser.flushInput()
	self.ser.flushOutput()

	self.command("C")

	# reset complete

  def getVersions(self):
	# debug
	self.fw_ver = self.command("v")
	self.hw_ver = self.command("V")
	#print 'HW: %s, FW: %s' % (self.hw_ver, self.fw_ver)


  def openCAN(self, speed=10000, mode='LISTENONLY'):
	speedChar = '0'
	if speed == 10000: speedChar = '0'
	elif speed == 20000: speedChar = '1'
	elif speed == 50000: speedChar = '2'
	elif speed == 100000: speedChar = '3'
	elif speed == 125000: speedChar = '4'
	elif speed == 250000: speedChar = '5'
	elif speed == 500000: speedChar = '6'
	elif speed == 800000: speedChar = '7'
	elif speed == 1000000: speedChar = '8'
	
	# open connection
	# Speed 10 kbaud
	reply = self.command("S%s" % speedChar)
	
	# LISTENONLY
	reply = self.command("L")


  def closeCAN(self):
	self.ser.flushInput()
	self.ser.flushOutput()
	self.command("C")
	time.sleep(0.1)
	self.ser.flushInput()
	self.ser.flushOutput()
	self.command("C")


  def readline(self):
	reply = ''
	c = ''
	while c != '\r':
		c = self.ser.read(1)
		if c and c != '\r':
			reply = reply + c
		if c == '\x07':
			print 'BELL'
			break
	return reply
	


  def command(self, cmd):
	if not cmd.endswith('\r'):
		cmd = cmd + '\r'
	self.ser.write(cmd)
	reply = self.readline()
	print 'DEBUG: reply to %s was %s' % (cmd[:-1], ['%s ' % hex(ord(c)) for c in reply])
	return reply


