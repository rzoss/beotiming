#===============================================================================
# SETUP

try:
  import ci2c # python2
except ImportError:
  from . import ci2c # python3

ci2c.initDefaults()  
  
class Portexpander:

	# Initialisieren von 8-Bit-I/O-expander
	def PCF8574_init(self):
		# IC3 adresse 0x21
		# IC3 P0, P1 als Output
		# IC3 P2, P3, P4, P5, P6, P7 als Input
		ci2c.write(0x21,[0xFC])
		# IC5 adresse 0x20
		# IC5 P0, P1, P2, P3, P4, P5, P6, P7 als Input
		ci2c.write(0x20,  [0xFF])
	
	# Zustand des Roten LED festlegen
	def set_LED_Rot(self, state):
		# LED ist an IC3 (adresse 0x21)
		result, buf = ci2c.read(0x21, 1)
		data = buf[0]
		# Aktueller zustand der LED's abfragen
		data = data & 0xFE
		data = state | data
		# Zustand der Roten LED aktualisieren
		ci2c.write(0x21, [data])
	
	# Zustand des Gruenen LED festlegen
	def set_LED_Gruen(self, state):
		# LED ist an IC3 (adresse 0x21)
		state = state << 1
		result, buf = ci2c.read(0x21, 1)
		data = buf[0]
		# Aktueller zustand der LED's abfragen
		data = data & 0xFD
		data = state | data
		# Zustand der Roten LED aktualisieren
		ci2c.write(0x21, [data])

	# Zustand der LED's festlegen
	def set_LED(self, state_Rot, state_Gruen):
		# LED's sind an IC3 (adresse 0x21)
		state_Gruen = state_Gruen << 1
		data = state_Rot | 0xFC
		data = state_Gruen | data
		# Zustand der LED's aktualisieren
		ci2c.write(0x21, [data])
	
	# Zustand der Rueck Taste auslesen
	def read_Rueck(self):
		# Taste ist an IC5 (adresse 0x20)
		result, buf = ci2c.read(0x20, 1)
		data = buf[0]
		data = data ^ 0xFF
		# Rückgabe des Tasten Zustandes
		if data & 0x10:
			return True
		else:
			return False

	# Zustand der OK Taste auslesen
	def read_OK(self):
		# Taste ist an IC5 (adresse 0x20)
		result, buf = ci2c.read(0x20, 1)
		data = buf[0]
		data = data ^ 0xFF
		# Rückgabe des Tasten Zustandes
		if data & 0x20:
			return True
		else:
			return False

	# Zustand der Vor Taste auslesen
	def read_Vor(self):
		# Taste ist an IC5 (adresse 0x20)
		result, buf = ci2c.read(0x20, 1)
		data = buf[0]
		data = data ^ 0xFF
		# Rückgabe des Tasten Zustandes
		if data & 0x40:
			return True
		else:
			return False

	# Zustand der Tasten auslesen
	# Rueckegabe Rueck_Taste 0x10
	# Rueckegabe OK_Taste 0x20
	# Rueckegabe Vor_Taste 0x40
	def read_Tasten(self):
		# Tasten sind an IC5 (adresse 0x20)
		result, buf = ci2c.read(0x20, 1)
		data = buf[0]
		# Rückgabe der Tasten Zustaende
		data = data ^ 0xFF
		if data & 0x10:
			return 0x01
		if data & 0x20:
			return 0x02
		if data & 0x40:
			return 0x04
		else:
			return 0x00