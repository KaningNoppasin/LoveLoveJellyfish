import serial

# Configure the serial port (replace 'COM3' with your port)
ser = serial.Serial(
    port='/dev/tty.usbserial-0001',          # Specify your port here
    baudrate=250000,        # Set your desired baud rate
    bytesize=serial.EIGHTBITS,  # 8-bit data
    parity=serial.PARITY_NONE,  # No parity
    stopbits=serial.STOPBITS_ONE  # 1 stop bit
)

# Check if the port is open
if ser.is_open:
    print("Serial port is open and configured.")

# Read data from the serial port
data = ser.read(10)  # Reads 10 bytes
print("Received data:", data)

# Send data to the serial port
ser.write(b'Hello')  # Sending data as bytes

# Close the serial port
ser.close()
