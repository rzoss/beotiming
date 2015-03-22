#===============================================================================
# SETUP
import spidev
import RPi.GPIO as GPIO
import time

class Display:
	#Display initialisieren
	def display_init(self):
		self.PIN_RS = 16
		self.PIN_CSB = 18
		self.PIN_RESET = 15
		self.PIN_LEDBACK = 13

		self.spi = spidev.SpiDev()

		# Initialisiere GPIO
		# Verwendet physische Pinnumern
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.PIN_RS, GPIO.OUT)
		GPIO.setup(self.PIN_CSB, GPIO.OUT)
		GPIO.setup(self.PIN_RESET, GPIO.OUT)
		GPIO.setup(self.PIN_LEDBACK, GPIO.OUT)

		# Display Steuerungs Pins einstellen
		self.display_RS(False)
		self.display_CSB(True)

		# Display Hintergrundbeleuchtung ausschalten
		self.display_backlight(False)

		# Reset
		self.display_RESET()

		# Aktiviert SPI modul
		self.spi.open(0,1)

		# Display Start sequenz
		time.sleep(0.04)#~40 ms
		self.display_CSB(False)
		# 0x39: 8-Bit Datenlaenge, 3 Zeilen, Instruction table 1
		# 0x15: BS: 1/5, 3-zeiliges LCD
		# 0x55: Booster ein, Kontrast C5, C4 setzen
		# 0x6E: Spannungsfolger und Verstaerkung setzen
		resp = self.spi.xfer2([0x39, 0x15, 0x55, 0x6E])
		time.sleep(0.3)#~300 ms
		# 0x70: Kontrast C3, C2, C1 setzen
		# 0x0C: Display ein, Cursor ein, Cursor blinken
		# 0x01: Display loeschen, Cursor Home
		# 0x06: Cursor Auto-Increment
		resp = self.spi.xfer2([0x70, 0x0C, 0x01])
		time.sleep(0.00003)#~30 us
		resp = self.spi.xfer2([0x06])
		self.display_CSB(True)
		time.sleep(0.00003)#~30 us

		# Display Hintergrundbeleuchtung einschalten
		self.display_backlight(True)
		self.display_backlight(True)
		# Display Inhalt loeschen
		self.clear_display()
		# SPI Uebertragung beenden
		self.spi.close()
		# Ende init

	def display_backlight(self, state):
		GPIO.output(self.PIN_LEDBACK, state)

	def display_RS(self, state):
		GPIO.output(self.PIN_RS, state)

	def display_CSB(self, state):
		GPIO.output(self.PIN_CSB, state)

	# Display zuruecksetzen
	def display_RESET(self):
		GPIO.output(self.PIN_RESET, False)
		GPIO.output(self.PIN_RESET, True)

	# Auf Display schreiben
	# Line = Zeile 1, 2 oder 3
	# Text = anzuzeigender Inhalt
	def display_write(self, zeile, text):
		self.zeile = zeile
		# Wandelt string zu int list um
		new_text = [ord(c) for c in text]
		# Cursor Position einstellen
		self.set_cursor()
 		self.spi.open(0,1)
		time.sleep(0.04)#~40 ms

		self.display_backlight(True)

		self.display_RS(True)
		self.display_CSB(False)

		# Text uebertragen
		resp = self.spi.xfer2(new_text)

		self.display_CSB(True)
		self.spi.close()

	# Cursor Position festlegen
	# 1. Zeile 0
	# 2. Zeile 1
	# 3. Zeile 2
	def set_cursor(self):
		self.spi.open(0,1)
		time.sleep(0.04)#~40 ms

		self.display_RS(False)
		self.display_CSB(False)

		# 1. Zeile DDRAM Adresse 0x00 bis 0xOF
		if self.zeile == 0:
			resp = self.spi.xfer2([0x80])
		# 2. Zeile DDRAM Adresse 0x10 bis 0x1F
		if self.zeile == 1:
			resp = self.spi.xfer2([0x90])
		# 3. Zeile DDRAM Adresse 0x20 bis 0x2F
		if self.zeile == 2:
			resp = self.spi.xfer2([0xA0])

		self.display_CSB(True)
		self.spi.close()

	# Display loeschen
	def clear_display(self):
		self.spi.open(0,1)
		time.sleep(0.04)#~40 ms

		self.display_RS(False)
		self.display_CSB(False)
		resp = self.spi.xfer2([0x01])

		self.display_CSB(True)
		self.spi.close()
