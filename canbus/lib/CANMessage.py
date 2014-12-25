#!/usr/bin/python
# -* coding: utf-8 *-


class CANMessage(object):
	def __init__(self, string):
		self.type = None
		self.databytes = []
		self.ext = False
		self.rtr = False
		self.valid = False
		self.raw = string

		mydata = ''
		datalength = 0
		if len(string) < 5:
			self.valid = False
			return
		type = string[0]
		if type in ('r', 't'):
			# simple (non-extended) CAN message
			if type == 'r':
				self.rtr = True
			try:
				self.type = int(string[1:4],16)
			except:
				self.valid = False
				return
			datalength = int(string[4])
			if not self.rtr:
				datastr = string[5:]
				if len(datastr) != datalength * 2:
					self.valid = False
					return
				for index in range(datalength):
					self.databytes.append(int(datastr[index*2:index*2+2],16))
			self.valid = True

		elif type in ('R', 'T'):
			self.valid = False
			print 'extended frames not supported!'
			

	
