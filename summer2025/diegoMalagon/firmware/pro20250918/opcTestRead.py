import opcDriver as opc
import time

def main():
    opc.opc_on()
    try:
        print("Device Info:", opc.opc_info())
        for i in range(5):
            pm = opc.opc_pm()
            print(f"Reading {i+1}: PM1={pm['PM1']:.2f}, PM2.5={pm['PM2.5']:.2f}, PM10={pm['PM10']:.2f}")
            hist = opc.opc_histogram()
            print("Histogram bins:", hist["bins"])
            time.sleep(2)
    finally:
        opc.opc_off()
        print("Device turned off.")

if __name__ == "__main__":
    main()
