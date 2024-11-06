import serial
import numpy as np
import time

# Serial port configuration
# Replace with the correct port (e.g., COM3 on Windows or /dev/ttyUSB0 on Linux/Mac)
SERIAL_PORT = '/dev/tty.usbserial-0001'
# SERIAL_PORT = '/dev/tty.usbserial-A5XK3RJT'
# BAUD_RATE = 115200            # Baud rate
# BAUD_RATE = 250_000            # Baud rate
BAUD_RATE = 1_000_000            # Baud rate
CHUNK = 1000                  # Number of audio samples to read at a time
SAMPLE_RATE = 44100           # Sample rate of the incoming audio data

# Initialize serial connection
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Allow some time for the serial connection to establish

print("Reading frequencies from UART... Press Ctrl+C to stop.")


try:
    while True:
        # Read audio data from UART
        # print("ser.in_waiting",ser.in_waiting)
        if ser.in_waiting >= CHUNK:  # Ensure we have enough data for FFT
            data = ser.read(CHUNK)

            # Convert 8-bit audio data to numpy array
            audio_data = np.frombuffer(data, dtype=np.uint8)

            # Normalize 8-bit data to -1 to 1 range (optional, depending on data source)
            audio_data = (audio_data - 128) / 128.0

            # Perform FFT on the audio data
            fft_data = np.fft.fft(audio_data)
            freqs = np.fft.fftfreq(len(fft_data), 1 / SAMPLE_RATE)

            # Calculate magnitudes and find the dominant frequency
            magnitudes = np.abs(fft_data)
            # Only consider positive frequencies
            dominant_freq = abs(freqs[np.argmax(magnitudes[:CHUNK // 2])])

            # Print the dominant frequency
            print(f"Real-time Dominant Frequency: {dominant_freq:.2f} Hz")

except KeyboardInterrupt:
    print("\nStopped reading from UART.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Ensure the serial connection is closed on exit
    ser.close()
