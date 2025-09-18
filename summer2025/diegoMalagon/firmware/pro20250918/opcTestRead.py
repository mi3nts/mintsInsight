# import opcDriver as opc
# from time import sleep

# def main():
#     opc.init()
#     opc.opc_on()
#     try:
#         print("Device Info:", opc.opc_info())
#         for i in range(5):
#             pm = opc.opc_pm()
#             print(f"Reading {i+1}: {pm}")
#             hist = opc.opc_histogram()
#             print(f"Histogram Bins: {hist['bins']}")
#             sleep(2)
#     finally:
#         opc.opc_off()
#         opc.cleanup()
#         print("Device turned off.")

# if __name__ == "__main__":
#     main()
from time import sleep
import opcng as opc
import spidev

spi = spidev.SpiDev()
spi.open(0, 0)
spi.mode = 1
spi.max_speed_hz = 2000000  # 2 MHz
spi.lsbfirst = False

# autodetect device
dev = opc.detect(spi)

# power on fan and laser
dev.on()

sleep(1)

for i in range(10):
    # query particle mass readings
    pm = dev.pm()

    for k, v in pm.items():
        print(f'{k}: {v}')

    sleep(1)

# power off fan and laser
dev.off()