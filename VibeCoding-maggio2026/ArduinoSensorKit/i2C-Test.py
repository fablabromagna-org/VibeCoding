import board                            # lib di circuit python
import busio
import time

#i2c = busio.I2C( board.GP9, board.GP8 ) # init della porta su pin specifici
i2c = busio.I2C( scl=board.GP21, sda=board.GP20 )

while not i2c.try_lock():
    pass
try:
    while True:
        print("I2C addresses found:", [hex(device_address)
              for device_address in i2c.scan()])
        time.sleep(2)
finally:  # uscite forzate dal programma devono garantire unlock della I2C
    i2c.unlock()

