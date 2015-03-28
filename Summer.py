import RPi.GPIO as GPIO
import time

PIN_A = 12

class summer:

	def init():
		# Initialisiere GPIO
		# Verwendet physische pin numbern
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(PIN_A, GPIO.OUT)

	def beep(zeit):
		# Initialisiere PWM an pwmPin mit frequenz 4kHz
		pwm = GPIO.PWM(PIN_A, 4000)
		pwm.start(0)
		# Tastgrad auf 50% einstellen
		pwm.ChangeDutyCycle(50)
		time.sleep(zeit)
		pwm.stop()

	
# Test Code	
init()
# Signal für 0.2 sec.
beep(0.2)
GPIO.cleanup()
print ("Beendet")
