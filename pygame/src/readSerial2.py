import serial
import time

# Configure the serial port
ser = serial.Serial(
    port='/dev/tty.usbserial-0001',  # Replace with your serial port name
    # baudrate=250000,
    baudrate=2000000,
    timeout=1
)

try:
    while True:
        if ser.in_waiting > 0:
            # Read data from UART and decode it
            data = ser.read(2)  # Read 2 bytes (assuming 12-bit data sent as two bytes)
            value = int.from_bytes(data, byteorder='little')
            print("ADC Value:", value)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    ser.close()
