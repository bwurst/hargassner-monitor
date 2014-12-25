#!/usr/bin/python
# -* coding: utf-8 *-

import urllib, urllib2
import time
import os, os.path

from config import smsconfig

def send_sms(message):
	if not smsconfig.enable:
		return
	now = int(time.time())
	files = os.listdir('sent')
	if len(files) > 0:
		files.sort()
		newest = files[-1]
		if newest > str(now - smsconfig.mindelay): 
			return
	params = {'UserKey': smsconfig.userkey,
		  'Password': smsconfig.password,
		  'Recipient': smsconfig.recipient,
		  'Originator': smsconfig.sender,
		  'MessageText': message}
	params = urllib.urlencode(params)
	print 'https://webservice.aspsms.com/aspsmsx.asmx/SimpleTextSMS?' + params
	response = urllib2.urlopen('https://webservice.aspsms.com/aspsmsx.asmx/SimpleTextSMS?' + params)
	answer = response.read()
	sent_file = open(os.path.join(smsconfig.sentfolder, '%s.log' % now), 'w')
	sent_file.write(message+'\n')
	sent_file.write(answer + '\n')
	sent_file.close()


