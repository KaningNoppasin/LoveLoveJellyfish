import serial
import numpy as np
import time
from collections import deque

# Serial configuration
SERIAL_PORT = '/dev/tty.usbserial-0001'      # Adjust as needed
BAUD_RATE = 2_000_000        # Set to match each 8-bit transmission's baud rate
# BAUD_RATE = 500000        # Set to match each 8-bit transmission's baud rate
TIMEOUT = 1               # Timeout for serial read in seconds

# FFT configuration
SAMPLE_SIZE = 1024        # Number of samples for FFT (adjustable)
# SAMPLING_RATE = 250000    # Effective data rate for complete 12-bit samples (Hz)
SAMPLING_RATE = 20000    # Effective data rate for complete 12-bit samples (Hz)
# SAMPLING_RATE = 40000    # Effective data rate for complete 12-bit samples (Hz)
start_time = time.time()
# Buffer for storing 12-bit ADC samples
sample_buffer = deque(maxlen=SAMPLE_SIZE)
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
except:
    print("Error Serial")
def read_uart_data():
    global start_time
    # Open the serial connection
    try:
        # while True:
            if ser.in_waiting >= 1:
                msb = ser.read(1)
                msb = int.from_bytes(msb, byteorder='big')
                sample_buffer.append(msb)
                if len(sample_buffer) == SAMPLE_SIZE:
                    start_time = time.time()
                    temp =  perform_fft_analysis(list(sample_buffer))
                    end_time = time.time()
                    elapsed_time_ms = (end_time - start_time) * 1000
                    # print(f"Runtime: {elapsed_time_ms:.3f} milliseconds")
                    return temp
    except KeyboardInterrupt:
        ser.close()
    return 0

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
    positive_magnitudes = np.abs(fft_result[:len(fft_result) // 4])
    
    # Identify the frequency with the maximum magnitude
    dominant_freq = positive_freqs[np.argmax(positive_magnitudes)]
    # index = np.argmax(positive_magnitudes)
    
    # dominant_freq /= 100
    # print(f"Dominant Frequency: {dominant_freq :.2f} Hz")
    return dominant_freq
    # return index

if __name__ == '__main__':
    try:
        print(f"Starting to read data from {SERIAL_PORT} at {BAUD_RATE} baud...")
        while True:
            data = read_uart_data() /2
            # data = read_uart_data()
            if data == 0: continue
            # if data > 10_000:
            #     continue
            # if data > 2_000:
            #     continue
            print(data)
            if data >500:
                # pyautogui.press('up')
                pass
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except Exception as e:
        print(f"Error: {e}")
