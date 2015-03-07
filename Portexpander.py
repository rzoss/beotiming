# Addressen     IC3: 0100 001 R/W (1/0)
#                       IC5: 0100 000 R/W (1/0)
# I2C max clock frequency 100kHz

# import I2C funktionen (veraenderungen moeglich)
import smbus
bus = smbus.SMBus(1)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
# I2C write funktion:   long write_byte(int addr,char val)
# I2C read funktion:    long read_byte(int addr)

import time


# I/O Expander Input write 1
# I/O Output write 1/0

# IC5 alle Input
# IC3 P0 & P1 Output Rest Input

def PCF8574_init():
        # IC3 0x21
        # IC5 0x20
        bus.write_byte(0x21, 0xFC)
        bus.write_byte(0x20, 0xFC)

def set_LED_Rot(state):
        # IC3 0x21
        data = bus.read_byte(0x21)
        data = data & 0xFE
        data = state | data
        bus.write_byte(0x21, data)

def set_LED_Gruen(state):
        # IC3 0x21
        state = state * 2
        data = bus.read_byte(0x21)
        data = data & 0xFD
        data = state | data
        bus.write_byte(0x21, data)

def set_LED(state_Rot, state_Gruen):
        # IC3 0x21
        state_Gruen = state_Gruen << state_Gruen
        data = state_Rot | 0xFC
        data = state_Gruen | data
        bus.write_byte(0x21, data)

def read_Rueck():
        # IC5 0x41
        data = bus.read_byte(0x20)
        if data & 0x10:
                return False
        else:
                return True

def read_OK():
        # IC5 0x41
        data = bus.read_byte(0x20)
        if data & 0x20:
                return False
        else:
                return True

def read_Vor():
        # IC5 0x41
        data = bus.read_byte(0x20)
        if data & 0x40:
                return False
        else:
                return True

def read_tasten():
        # IC5 0x41
        data = bus.read_byte(0x20)
        if (data & 0x10)^0xFF:
                return 0x01
        if (data & 0x20)^0xFF:
               return 0x02
        if (data & 0x40)^0xFF:
               return 0x04
        else:
                return 0x00


#       data = data & 0x70
#       data = data ^ 0x70
#       data = data >> data
#       data = data >> data
#       data = data >> data
#       data = data >> data
#       return data



# ++++++++++++ Test Code +++++++++++++++++++++++++++++++++++++++++

PCF8574_init()
time.sleep(1)
x = 6000
while x:
       if read_OK():
               set_LED_Gruen(1)
               set_LED_Rot(0)
       else:
               set_LED_Gruen(0)
               set_LED_Rot(1)
        time.sleep(0.001)
        x = x - 1
