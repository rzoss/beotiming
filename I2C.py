import smbus
import time

# I2C-Adresse
address = 0x50

# Erzeugen einer I2C-Instanz
Test = smbus.SMBus(1)

#res = Test.write_i2c_block_data(address, 0x01, [0x00])
#print(res)
res = Test.read_i2c_block_data(address,0x01)
print 'RFID at address 0x{0:02x} READ 0x{1:04x}'.format( address, res )
