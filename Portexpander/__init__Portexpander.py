# Addressen     IC3: 0100 001 R/W (1/0)
#                       IC5: 0100 000 R/W (1/0)
# I2C max clock frequency 100kHz

# import I2C funktionen (veraenderungen moeglich)
import smbus
bus = smbus.SMBus(1)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
# I2C write funktion:   long write_byte(int addr,char val)
# I2C read funktion:    long read_byte(int addr)

class Portexpander

	# Initialisieren von 8-Bit-I/O-expander
	def PCF8574_init(self):
		# IC3 adresse 0x21
		# IC3 P0, P1 als Output
		# IC3 P2, P3, P4, P5, P6, P7 als Input
		bus.write_byte(0x21, 0xFC)
		# IC5 adresse 0x20
		# IC5 P0, P1, P2, P3, P4, P5, P6, P7 als Input
		bus.write_byte(0x20, 0xFF)
	
	# Zustand des Roten LED festlegen
	def set_LED_Rot(self, state):
		# LED ist an IC3 (adresse 0x21)
		data = bus.read_byte(0x21)
		# Aktueller zustand der LED's abfragen
		data = data & 0xFE
		data = state | data
		# Zustand der Roten LED aktualisieren
		bus.write_byte(0x21, data)
	
	# Zustand des Gruenen LED festlegen
	def set_LED_Gruen(self, state):
		# LED ist an IC3 (adresse 0x21)
		state = state << 1
		data = bus.read_byte(0x21)
		# Aktueller zustand der LED's abfragen
		data = data & 0xFD
		data = state | data
		# Zustand der Roten LED aktualisieren
		bus.write_byte(0x21, data)

	# Zustand der LED's festlegen
	def set_LED(self, state_Rot, state_Gruen):
		# LED's sind an IC3 (adresse 0x21)
		state_Gruen = state_Gruen << 1
		data = state_Rot | 0xFC
		data = state_Gruen | data
		# Zustand der LED's aktualisieren
		bus.write_byte(0x21, data)
	
	# Zustand der Rueck Taste auslesen
	def read_Rueck(self):
		# Taste ist an IC5 (adresse 0x20)
		data = bus.read_byte(0x20)
		data = data ^ 0xFF
		# Rückgabe des Tasten Zustandes
		if data & 0x10:
			return True
		else:
			return False

	# Zustand der OK Taste auslesen
	def read_OK(self):
		# Taste ist an IC5 (adresse 0x20)
		data = bus.read_byte(0x20)
		data = data ^ 0xFF
		# Rückgabe des Tasten Zustandes
		if data & 0x20:
			return True
		else:
			return False

	# Zustand der Vor Taste auslesen
	def read_Vor(self):
		# Taste ist an IC5 (adresse 0x20)
		data = bus.read_byte(0x20)
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
		data = bus.read_byte(0x20)
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