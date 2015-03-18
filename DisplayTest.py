import spidev
import RPi.GPIO as GPIO
import time

PIN_RS = 16
PIN_CSB = 18
PIN_RESET = 15
PIN_LEDBACK = 13

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_RS, GPIO.OUT)
GPIO.setup(PIN_CSB, GPIO.OUT)
GPIO.setup(PIN_RESET, GPIO.OUT)
GPIO.setup(PIN_LEDBACK, GPIO.OUT)

GPIO.output(PIN_RS, False)
GPIO.output(PIN_CSB, True)
GPIO.output(PIN_LEDBACK, False)

# Reset
GPIO.output(PIN_RESET, True)
GPIO.output(PIN_RESET, False)
GPIO.output(PIN_RESET, True)

spi = spidev.SpiDev()

# open /dev/spidev0.0
spi.open(0,0)


# Display init
# Display Start sequenz

time.sleep(0.04)#~40 ms

# writebytes
# Syntax: write([values])
# Returns: None
# Description: Write bytes to SPI device.

# xfer
# Syntax: xfer([values])
# Returns: [values]
# Description: Perform SPI transaction. CS released and reactivated between blocks

# xfer2
# Syntax: xfer2([values])
# Returns: [values]
# Description: Perform SPI transaction. CS will be held active between blocks.

#resp = spi.xfer2([0x39])
#time.sleep(0.00003)#~30 us

#resp = spi.xfer2([0x15])
#time.sleep(0.00003)#~30 us

#resp = spi.xfer2([0x55])
#time.sleep(0.00003)#~30 us

#resp = spi.xfer2([0x6E])
#time.sleep(0.3)#~300 ms

#resp = spi.xfer2([0x72])
#time.sleep(0.00003)#~30 us

#resp = spi.xfer2([0x0F])
#time.sleep(0.00003)#~30 us

#resp = spi.xfer2([0x01])
#time.sleep(0.00003)#~30 us

#resp = spi.xfer2([0x06])
#time.sleep(0.00003)#~30 us
GPIO.output(PIN_CSB, False)

# 0x39: 8-Bit Datenlänge, 3 Zeilen, Instruction table 1
# 0x15: BS: 1/5, 3-zeiliges LCD
# 0x55: Booster ein, Kontrast C5, C4setzen
# 0x6E: Spannungsfolger und Verstärkung setzen
resp = spi.xfer2([0x39, 0x15, 0x55, 0x6E])
time.sleep(0.3)#~300 ms
# 0x70: Kontrast C3, C2, C1 setzen
# 0x0C: Display ein, Cursor ein, Cursor blinken
# 0x01: Display löschen, Cursor Home
# 0x06: Cursor Auto-Increment
resp = spi.xfer2([0x70, 0x0C, 0x01])
time.sleep(0.00003)#~30 us
resp = spi.xfer2([0x06])
GPIO.output(PIN_CSB, True)
time.sleep(0.00003)#~30 us

# Ende init

# Backlight on
GPIO.output(PIN_LEDBACK, True)
# RS high to send data
GPIO.output(PIN_RS, True)

# CS low
GPIO.output(PIN_CSB, False)
# send "HelloWorld"
resp = spi.xfer2([0x48, 0x65, 0x6C, 0x6C, 0x6F, 0x20, 0x57, 0x6F, 0x72, 0x6C, 0x64, 0x20, 0x23, 0x31, 0x20, 0x20])
resp = spi.xfer2([0x48, 0x65, 0x6C, 0x6C, 0x6F, 0x20, 0x57, 0x6F, 0x72, 0x6C, 0x64, 0x20, 0x23, 0x32, 0x20, 0x20])
resp = spi.xfer2([0x48, 0x65, 0x6C, 0x6C, 0x6F, 0x20, 0x57, 0x6F, 0x72, 0x6C, 0x64, 0x20, 0x23, 0x33, 0x20, 0x20])
# CS high
GPIO.output(PIN_CSB, True)
input('Press return to stop:')   # use raw_input for Python 2

# Backlight off
GPIO.output(PIN_LEDBACK, False)

spi.close()

print ("Beendet")

