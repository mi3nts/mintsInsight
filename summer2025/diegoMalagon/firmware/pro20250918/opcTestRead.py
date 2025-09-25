import csv, time
import opcDriver as opc

def main():
    opc.init()
    opc.opcOn()
    time.sleep(2)

    with open("opc_log.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "cmd", "mode", "raw_bytes"])

        try:
            while True:
                ts = time.time()
                pm = opc.opcPm()
                hist = opc.opcHistogram()

                writer.writerow([ts, "PM", "raw", pm])
                writer.writerow([ts, "HIST", "raw", hist])
                f.flush()

                time.sleep(1)

        except KeyboardInterrupt:
            print("Stopping...")
        finally:
            opc.opcOff()
            opc.cleanup()

if __name__ == "__main__":
    main()
