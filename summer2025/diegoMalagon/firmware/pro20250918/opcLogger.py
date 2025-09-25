import csv, time
import opcDriver as opc

def log_data(filename="opc_log.csv"):
    opc.init()
    opc.opcOn()
    time.sleep(10)  # warm-up

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        # header
        writer.writerow(["timestamp", "PM1", "PM2.5", "PM10"] + [f"bin{i}" for i in range(16)])

        try:
            while True:
                pm = opc.opcPm()
                hist = opc.opcHistogram()

                # only log if data has non-zeros
                if pm and hist and (any(hist) or any(pm)):
                    ts = time.strftime("%Y-%m-%d %H:%M:%S")
                    row = [ts, pm[0], pm[1], pm[2]] + hist[:16]
                    writer.writerow(row)
                    f.flush()
                    print("Logged:", row)

                time.sleep(5)  # adjust interval

        except KeyboardInterrupt:
            print("Logging stopped by user.")
        finally:
            opc.opcOff()
            opc.cleanup()
