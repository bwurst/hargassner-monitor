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
		self.stoerung           = False
		self.stoerungsnummer	= 0
		self.raumaustragung	= 0
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
			self.stoerung 		= bool(int(e[100], 16) & 0x800) # Interpretiere als hex und verschneide mit 0x800
			self.stoerungsnummer	= int(e[98]) # Stoerungsnummer
			self.raumaustragung	= bool(int(e[99], 16) & 0x101)
		except:
			pass

