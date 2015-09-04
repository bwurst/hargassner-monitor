# -* coding: utf-8 *-


class Parser(object):
	def __init__(self, string):
		if not string.startswith('pm '):
			return False
		self.elements = string.split(' ')
		e = self.elements
		self.saugzuggeblaese    = 0
		self.pufferladepumpe    = False
		self.o2                 = 0
		self.kesseltemperatur   = 0
		self.rauchgastemperatur = 0
		self.aussentemperatur   = 0
		self.aussen_mittel      = 0
		self.puffer_oben        = 0
		self.puffer_unten       = 0
		self.kessel_soll        = 0
		self.anforderung        = 0
		try:
			self.saugzuggeblaese    = e[1]
			self.pufferladepumpe    = (e[2] == '1')
			self.o2                 = e[3]
			self.kesseltemperatur   = e[4]
			self.rauchgastemperatur = e[5]
			self.aussentemperatur   = e[6]
			self.aussen_mittel      = e[7]
			self.kessel_soll        = e[15]
			self.puffer_oben        = e[41]
			self.puffer_unten       = e[42]
			self.anforderung        = e[75]
		except:
			pass

