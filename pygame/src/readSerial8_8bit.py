import serial
import numpy as np
import time
from collections import deque

# Serial configuration
SERIAL_PORT = '/dev/tty.usbserial-0001'      # Adjust as needed
BAUD_RATE = 500000        # Set to match each 8-bit transmission's baud rate
TIMEOUT = 1               # Timeout for serial read in seconds

# FFT configuration
SAMPLE_SIZE = 1024        # Number of samples for FFT (adjustable)
SAMPLING_RATE = 250000    # Effective data rate for complete 12-bit samples (Hz)

# Buffer for storing 12-bit ADC samples
sample_buffer = deque(maxlen=SAMPLE_SIZE)

def assemble_12bit_value(msb, lsb):
    """
    Combine the two 8-bit segments into a single 12-bit value.
    """
    return (msb << 4) | (lsb >> 4)

def read_uart_data():
    # Open the serial connection
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT) as ser:
        while True:
            if ser.in_waiting >= 1:
                # Read two bytes for each 12-bit ADC sample
                msb = ser.read(1)
                
                # Convert to integer values
                msb = int.from_bytes(msb, byteorder='big')
                
                # Assemble the 12-bit value
                # adc_value = assemble_12bit_value(msb, lsb)
                
                # Store value in buffer
                sample_buffer.append(msb)
                
                # Process data if we have enough samples
                if len(sample_buffer) == SAMPLE_SIZE:
                    perform_fft_analysis(list(sample_buffer))

def perform_fft_analysis(samples):
    """
    Perform FFT analysis on the provided samples and print the dominant frequency.
    """
    # Convert samples to numpy array and apply FFT
    data = np.array(samples) - np.mean(samples)
    fft_result = np.fft.fft(data)
    freqs = np.fft.fftfreq(len(fft_result), 1 / SAMPLING_RATE)
    
    # Use only the positive half of the FFT result (real frequencies)
    positive_freqs = freqs[:len(freqs) // 2]
    positive_magnitudes = np.abs(fft_result[:len(fft_result) // 2])
    
    # Identify the frequency with the maximum magnitude
    dominant_freq = positive_freqs[np.argmax(positive_magnitudes)]
    
    dominant_freq /= 100
    print(f"Dominant Frequency: {dominant_freq :.2f} Hz")

if __name__ == '__main__':
    try:
        print(f"Starting to read data from {SERIAL_PORT} at {BAUD_RATE} baud...")
        read_uart_data()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except Exception as e:
        print(f"Error: {e}")
