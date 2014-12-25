#!/usr/bin/python
# -* coding: utf-8 *-

import datetime
import time
import serial
import os, sys

mypath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, mypath)

from lib.USBtin import USBtin
from lib.CANMessage import CANMessage
from lib import SMS


log = False
if len(sys.argv) > 1 and sys.argv[1] == '--log':
	log = True
if log:
	file_kessel = open('kessel.log', 'a')
	file_hkr1 = open('hkr1.log', 'a')
	file_hkr2 = open('hkr2.log', 'a')
	file_a = open('a.log', 'a')
file_other = open('other.log', 'a')
file_anforderung = open('anforderung.log', 'a')
anforderung = {1: 0, 2: 0}
s = USBtin('/dev/ttyACM0')
s.openCAN(50000)
try:
	while True:
		msg = CANMessage(s.readline())
		timestamp = datetime.datetime.now().isoformat()
		if msg.valid:
			logstr = msg.raw + ' ' + timestamp + ' ' + '%03x' % msg.type + ' ' + ' '.join(['%02x' % b for b in msg.databytes])
			if msg.type == 10:
				if msg.databytes[0] in [0x00, 0x01] and msg.databytes[1] == 0x00 and msg.databytes[4] == msg.databytes[7]:
					hkr = msg.databytes[0]+1
					text = None
					if msg.databytes[4] == 0x00:
						# keine Anforderung
						if anforderung[hkr] != 0:
							text = 'Anforderung HKR %i beendet' % hkr
							anforderung[hkr] = 0
					else:
						# Anforderung da
						if anforderung[hkr] != msg.databytes[4]: 
							text = 'Anforderung HKR %i auf %i°C' % (msg.databytes[0]+1, msg.databytes[4])
							anforderung[hkr] = msg.databytes[4]
					if text:
						file_anforderung.write(timestamp + ' ' + text+'\n')
						file_anforderung.flush()
						os.fsync(file_anforderung.fileno())
				if log:
					file_a.write(logstr + '\n')
					file_a.flush()
					os.fsync(file_a.fileno())
			elif msg.type == 20:
				timestamp = None
				stoerung = False
				rauchfangkehrer = False
				if msg.databytes[0] in [0x00, 0x01] and msg.databytes[1] == 0x00:
					timestamp = int(''.join(['%02x' % b for b in msg.databytes[4:]]),16)
					# Sekunden seit 1.1.1980
				if msg.databytes[0] in [0x00, 0x01] and msg.databytes[1] == 0x01:
					stoerung = bool(msg.databytes[6] & 0x01)
					rauchfangkehrer = bool(msg.databytes[5] & 0x01)
				add = ''
				if timestamp:
					realts = datetime.datetime(1980,1,1,0,0,0) + datetime.timedelta(seconds=timestamp)
					add = '    Es ist %s' % realts.isoformat()
				if stoerung: 
					add = '    STOERUNG!'
					SMS.send_sms('Stoerung an der Heizung!')
				if rauchfangkehrer: 
					add += '    Rauchfangkehrer-Modus'
				if log:
					file_kessel.write(logstr + add + '\n')
					file_kessel.flush()
					os.fsync(file_kessel.fileno())
			elif msg.type in [0x161, 0x14d]:
				if log:
					file_hkr1.write(logstr + '\n')
					file_hkr1.flush()
					os.fsync(file_hkr1.fileno())
			elif msg.type in [0x162, 0x14e]:
				if log:
					file_hkr2.write(logstr + '\n')
					file_hkr2.flush()
					os.fsync(file_hkr2.fileno())
			else:
				file_other.write(logstr + '\n')
				file_other.flush()
				os.fsync(file_other.fileno())
except:
	import traceback
	traceback.print_exc()
	pass
finally:
	s.closeCAN()

		
