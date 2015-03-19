import spidev
import RPi.GPIO as GPIO
import time

PIN_RS = 16
PIN_CSB = 18
PIN_RESET = 15
PIN_LEDBACK = 13

spi = spidev.SpiDev()

# Display initialisieren
def display_init():
	# Initialisiere GPIO
	# Verwendet physische pin numbern
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(PIN_RS, GPIO.OUT)
	GPIO.setup(PIN_CSB, GPIO.OUT)
	GPIO.setup(PIN_RESET, GPIO.OUT)
	GPIO.setup(PIN_LEDBACK, GPIO.OUT)
	
	# Display Steuerungs Pins einstellen
	display_RS(False)
	display_CSB(True)
	
	# Display Hintergrundbeleuchtung ausschalten
	display_backlight(False)

	# Reset
	display_RESET()

	# Aktiviert SPI modul
	spi.open(0,1)

	# Display Start sequenz
	time.sleep(0.04)#~40 ms
	display_CSB(False)
	# 0x39: 8-Bit Datenlaenge, 3 Zeilen, Instruction table 1
	# 0x15: BS: 1/5, 3-zeiliges LCD
	# 0x55: Booster ein, Kontrast C5, C4setzen
	# 0x6E: Spannungsfolger und Verstaerkung setzen
	resp = spi.xfer2([0x39, 0x15, 0x55, 0x6E])
	time.sleep(0.3)#~300 ms
	# 0x70: Kontrast C3, C2, C1 setzen
	# 0x0C: Display ein, Cursor ein, Cursor blinken
	# 0x01: Display loeschen, Cursor Home
	# 0x06: Cursor Auto-Increment
	resp = spi.xfer2([0x70, 0x0C, 0x01])
	time.sleep(0.00003)#~30 us
	resp = spi.xfer2([0x06])
	display_CSB(True)
	time.sleep(0.00003)#~30 us
	
	# Display Hintergrundbeleuchtung einschalten
	display_backlight(True)
	# SPI Ã¼bertragung beenden
	spi.close()
	# Ende init

def display_backlight(state):
	GPIO.output(PIN_LEDBACK, state)

def display_RS(state):
	GPIO.output(PIN_RS, state)

def display_CSB(state):
	GPIO.output(PIN_CSB, state)

# Display ZurÃ¼cksetzen
def display_RESET():
	GPIO.output(PIN_RESET, False)
	GPIO.output(PIN_RESET, True)

# Auf Display schreiben
# line = Zeile 1, 2 oder 3
# text = Anzuzeigender Inhalt
def display_write(Zeile, text):
	# Wandelt string zu int list um
	new_text = [ord(c) for c in text]
	# Cursor position einstellen
	set_cursor(Zeile)

	spi.open(0,1)
	time.sleep(0.04)#~40 ms

	display_backlight(True)
	
	display_RS(True)
	display_CSB(False)
	
	# Text Ã¼bertragen
	resp = spi.xfer2(new_text)

	display_CSB(True)
	spi.close()

# Cursor position festlegen
# 1. Zeile 0
# 2. Zeile 1
# 3. Zeile 2
def set_cursor(Zeile):
	spi.open(0,1)
	time.sleep(0.04)#~40 ms

	display_RS(False)
	display_CSB(False)
	
	# 1. Zeile DDRAM Adresse â€œ00Hâ€� to â€œOFHâ€�
	if Zeile == 0:
		resp = spi.xfer2([0x80])
	# 2. Zeile DDRAM Adresse â€œ10Hâ€� to â€œ1FHâ€�
	if Zeile == 1:
		resp = spi.xfer2([0x90])
	# 3. Zeile DDRAM Adresse â€œ20Hâ€� to â€œ2FHâ€�
	if Zeile == 2:
		resp = spi.xfer2([0xA0])

	display_CSB(True)
	spi.close()

# Display lÃ¶schen
def clear_display():
	spi.open(0,1)
	time.sleep(0.04)#~40 ms

	display_RS(False)
	display_CSB(False)
	resp = spi.xfer2([0x01])

	display_CSB(True)
	spi.close()

	
#Test Code
	
display_init()
time.sleep(1)
display_write(0, "Hallo Welt #0")
display_write(1, "Hallo Welt #1")
display_write(2, "Hallo Welt #2")
time.sleep(5)
clear_display()
time.sleep(1)
display_backlight(False)
GPIO.cleanup()
spi.close()
