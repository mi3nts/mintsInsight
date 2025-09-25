# opcTestRead.py
import opcDriver as opc
import opcLogger as logger
from time import sleep

def dump_bytes(label, resp):
    """Pretty print raw bytes as both decimal and hex"""
    print(f"{label} (len={len(resp)}):")
    print("dec:", resp)
    print("hex:", [hex(b) for b in resp])

def main():
    opc.init()
    opc.opcOn()
    print("Serial: ", opc.opcSerial())
    print("Warming up OPC... (10s)")
    sleep(10)

    try:
        while True:
            # --- PM Frame ---
            pm_resp = opc.spiTransfer(opc.cmdPm, 32)  # over-read
            dump_bytes("PM raw", pm_resp)

            # --- Histogram Frame ---
            hist_resp = opc.spiTransfer(opc.cmdHist, 128)  # over-read
            dump_bytes("Hist raw", hist_resp)

            print("-" * 60)
            # Log data using the logger module
            logger.log_data("opc_test_log.csv")

            sleep(2)

    except KeyboardInterrupt:
        print("\nStopping test...")

    finally:
        opc.opcOff()
        opc.cleanup()
        print("Device turned off.")

if __name__ == "__main__":
    main()
