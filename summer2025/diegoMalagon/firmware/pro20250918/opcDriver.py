import spidev

spi = spidev.SpiDev()
spi.open(0, 0)  # try (0,1) if this fails
spi.max_speed_hz = 100000

# send a simple read command (0x3F is "firmware version" for OPC)
resp = spi.xfer2([0x3F] + [0x00]*60)
print(resp)
