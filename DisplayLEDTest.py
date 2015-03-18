
import RPi.GPIO as GPIO
import time

PIN_LED = 13


GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_LED, GPIO.OUT)


GPIO.output(PIN_LED, True)

time.sleep(1)

GPIO.output(PIN_LED, False)

time.sleep(1)

GPIO.output(PIN_LED, True)

time.sleep(1)

GPIO.output(PIN_LED, False)

time.sleep(1)

print("Beendet")