# Piera IPS‑7100 I²C Interface (firmware ≥ V2.0.10)

## Electrical Interface & Address  
The IPS‑7100 uses open-drain I²C lines (SDA/SCL) with **built-in 4.7 kΩ pull‑ups**.  Cable lengths should be kept short (<10 cm) to avoid interference.  The 7-bit I²C address is **0x4B**, so write transactions use byte `0x96` and reads use `0x97` (address<<1 + R/W).

## I²C Protocol & Framing  
Communications use a “polling” master-driven style.  A **write** transaction consists of: `Start, [0x4B]<<1|0, Command, (Parameters), Stop`.  After any write, **wait ≥1 s before the next write**.  A **read** transaction is done with a repeated-start:
```
Start, Addr+W, Command, Sr (repeat start), Addr+R, Data1…DataN, Nack, Stop
```
The data bytes are returned in the order listed in the tables below.  All multi-byte values are transmitted MSB first (unless noted).

## Write Commands (Master → Sensor)  
Supported write commands (Table 6) include control and config operations. Each command has 0–4 data bytes as parameters:

- **0x10** – *Start/Stop Measurement*. 1-byte parameter 0–3: “0” = stop, “1”=start with 200 ms sampling, “2”=500 ms, “3”=1000 ms. (Sending 0x10 resets sampling – allow ≈5 s warm-up.)
- **0x21** – *Set Cleaning Interval*. Four bytes [n1,n2,n3,n4] as a 32-bit unsigned integer (seconds).
- **0x23** – *Power Saving Mode*. 1 byte: 0x01 = enter low‑power (≈273 µA), 0x00 = wake up. (Also resets sampling; allow ≈5 s warm-up.)
- **0x24** – *Set Data Unit*. 1 byte: selects output units (0=#/L,1=#/ft³,2=#/m³,3=#/L for PC; similarly 0–3 for PM).
- **0x26** – *Set Vth (Voltage Threshold)*. Two bytes [MSB,LSB] as a 16-bit value.
- **0x29** – *Set Vref (Vref Voltage)*. Two bytes [MSB,LSB].
- **0x2B** – *Fan Operation*. 1 byte: 0x01 = start fan, 0x00 = stop fan.
- **0x2C** – *Start Cleaning*. 1 byte: 0x01 = start cleaning cycle, 0x00 = stop.
- **0x2D** – *Reset*. No parameters. Soft-reset the sensor (≈5 s delay for re-init).
- **0x2E** – *Factory Reset*. No parameters. Restore defaults.

> **Note:** Always pause ≈1 s between write commands. After 0x10 or 0x23, allow ≈5 s for warm-up before reading data.

## Read Commands (Sensor → Master)  
All read commands use the format above and return data + CRC16. The length depends on the command. Key commands for measurement data:

- **0x11** – *Read PC (Particle Count) Data*. Returns 4-byte unsigned counts for all bins, plus a 2-byte CRC. Number of bins depends on model (3, 5, or 7). Thus total bytes = 4×N + 2. Each 4‑byte block is an unsigned 32‑bit count (MSB first).
- **0x12** – *Read PM (Mass) Data*. Returns 4-byte IEEE‑754 floats for all bins, plus 1 event code byte and 2 CRC bytes. There are N bins (3/5/7) as above, so total = 4×N + 3. **Data bytes are little-endian**: each 4‑byte group must be reversed to form a float. After the bin data comes 1 “event” byte, then 2 CRC bytes.
- **0x61** – *Read Cleaning Interval*. Returns 4-byte uint (seconds) + 2-byte CRC.
- **0x64** – *Read Data Unit*. Returns 1-byte unit code + 2-byte CRC.
- **0x65** – *Read Start/Stop (Measurement Period)*. Returns 2-byte period (ms) + 2-byte CRC.
- **0x66** – *Read Vth*. Returns 2-byte Vth + 2-byte CRC.
- **0x69** – *Read Vref*. Returns 2-byte Vref + 2-byte CRC.
- **0x6A** – *Read Status*. Returns 1 status byte + 2-byte CRC. (Bits: b0=fan, b1=cleaning, b2=PSM, b3=UART/I²C, etc.)
- **0x77** – *Read Serial Number*. Returns 17 bytes ASCII + 2-byte CRC.
- **0x78** – *Read Version*. Returns 7 bytes ASCII + 2-byte CRC.
- **0x79** – *Read Network Key*. Returns 24 bytes + 2-byte CRC.

For all reads, the last two bytes are a **CRC16** checksum (MSB, LSB) over the preceding data bytes.

## CRC16 Checksum  
The CRC uses polynomial **0x8408** (reverse of 0x1021). It is calculated with initial value 0xFFFF, processed bit‑wise, then bitwise-inverted and the bytes swapped. In practice, to verify data, compute CRC16 over the returned data (excluding the CRC bytes) and compare to `[CRC_high<<8 | CRC_low]` at the end of the packet.

## Data Formats and Endianness  
- **Particle Counts (0x11)**: Each bin count is a 32-bit unsigned integer (MSB first). In Python you can do `int.from_bytes(count_bytes, byteorder='big')`.
- **Mass Concentrations (0x12)**: Each bin value is a 4-byte float. The sensor transmits **little-endian** IEEE-754. E.g. if you read bytes `[A,B,C,D]`, interpret as `struct.unpack('<f', bytes([A,B,C,D]))`.
- **Event Byte (0x12)**: One byte indicating detected events (0=nothing,1=event,2=smoke,3=vape, etc) precedes the CRC.
- **Configuration/Status Reads**: Single/multi-byte values are big‑endian (MSB first) as shown. ASCII fields (serial/version) are plain bytes.

## Python Integration (SMBus2/Periphery)  
On a Raspberry Pi, use the `smbus2` or `periphery` libraries to send these I²C commands. For example, with `smbus2`:

- **Write a command** (e.g. start sampling):
  ```python
  bus = SMBus(1)
  addr = 0x4B
  bus.write_i2c_block_data(addr, 0x10, [0x01])  # send 0x10,0x01
  time.sleep(5)  # wait for sensor warm-up
  ```
  
- **Read data**: perform a write-then-read. Since SMBus has read functions that take a “register”, one approach is:
  ```python
  # Request PC data (command 0x11), then read 14 bytes (3 bins + CRC)
  bus.write_byte(addr, 0x11)
  raw = bus.read_i2c_block_data(addr, 0, 14)
  ```
  Or with `smbus2.i2c_msg`:
  ```python
  write = i2c_msg.write(addr, [0x11])
  read = i2c_msg.read(addr, 14)
  bus.i2c_rdwr(write, read)
  raw = list(read)
  ```
- **Parse returned bytes**: For 3-bin PC data, `raw[0:4]` is bin1, `raw[4:8]` bin2, `raw[8:12]` bin3, and `raw[12:14]` is CRC. Convert counts by:
  ```python
  counts = [int.from_bytes(raw[i:i+4], byteorder='big') for i in (0,4,8)]
  crc = (raw[12] << 8) | raw[13]
  ```
  For 3-bin PM data (command 0x12, total 4*3+3=15 bytes), do:
  ```python
  # raw[0:12] = 3 floats (little-endian), raw[12] = event, raw[13:15] = CRC
  floats = [struct.unpack('<f', bytes(raw[i:i+4]))[0] for i in (0,4,8)]
  event = raw[12]
  crc = (raw[13]<<8) | raw[14]
  ```
- **General tips**: Always respect the 1 s delay between writes. If using `periphery.I2C`, use similar write/read calls. Check CRC on each read to ensure data integrity.

## Example I²C Transactions  
For illustration, assume a 3‑bin device (IPS‑3100) and reading PC counts:

1. **Start Sampling** – master writes:
   ```
   Start, 0x96 (addr<<1|W), 0x10, 0x01, Stop  
   ```
   (Command 0x10 with parameter 1 for 200 ms sampling.)

2. **Wait ~5 s** for sensor warm-up.

3. **Read PC Data** – master sends repeated-start read:
   ```
   Start, 0x96, 0x11, Sr, 0x97, [Data: b0,b1,…,b13], Stop
   ```
   The sensor returns 14 bytes: 3×4 bytes counts + 2 bytes CRC. For example, suppose the sensor returns:
   ```
   00 00 00 64   00 00 00 C8   00 00 01 2C   12 34
   ```
   This splits into counts = `[0x00000064, 0x000000C8, 0x0000012C]` = `[100, 200, 300]`, with CRC16 = `0x1234`.

4. **Interpretation** – the counts are plain integers (100, 200, 300). In Python:
   ```python
   counts = [int.from_bytes(raw[i:i+4], 'big') for i in (0,4,8)]
   ```

A similar sequence with command **0x12** would read PM values as floats (little-endian) plus an event byte. Always verify the CRC16 at the end of each read.
