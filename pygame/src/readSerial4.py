import serial
import time

# Configure the serial connection
SERIAL_PORT = '/dev/tty.usbserial-0001'  # Replace with the correct port for your system
BAUD_RATE = 2000000  # 2 Mbps, as specified in your code
TIMEOUT = 1          # Read timeout in seconds

def receive_data():
    # Initialize the serial connection
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT) as ser:
        while True:
            # Read one byte at a time
            if ser.in_waiting > 0:
                data = ser.read(1)
                
                # Convert byte to integer
                byte_value = int.from_bytes(data, byteorder='big')
                
                # Process the received byte based on your protocol
                print(f"Received byte: {byte_value:02X}")
            
            # Optional: wait for a short period to avoid high CPU usage
            time.sleep(0.01)

if __name__ == '__main__':
    try:
        print(f"Starting to read data from {SERIAL_PORT} at {BAUD_RATE} baud...")
        receive_data()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except Exception as e:
        print(f"Error: {e}")
