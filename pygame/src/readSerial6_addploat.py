import serial
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

# Serial configuration
SERIAL_PORT = '/dev/tty.usbserial-0001'      # Adjust as needed
BAUD_RATE = 500000        # Set to match each 8-bit transmission's baud rate
TIMEOUT = 1               # Timeout for serial read in seconds

# FFT and Plotting configuration
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
            if ser.in_waiting >= 2:
                # Read two bytes for each 12-bit ADC sample
                msb = ser.read(1)
                lsb = ser.read(1)
                
                # Convert to integer values
                msb = int.from_bytes(msb, byteorder='big')
                lsb = int.from_bytes(lsb, byteorder='big')
                
                # Assemble the 12-bit value
                adc_value = assemble_12bit_value(msb, lsb)
                
                # Store value in buffer
                sample_buffer.append(adc_value)
                
                # Process data if we have enough samples
                if len(sample_buffer) == SAMPLE_SIZE:
                    perform_fft_analysis(list(sample_buffer))
                    plot_data(list(sample_buffer))

def perform_fft_analysis(samples):
    """
    Perform FFT analysis on the provided samples and print the dominant frequency.
    """
    # Convert samples to numpy array and remove DC offset
    data = np.array(samples) - np.mean(samples)
    fft_result = np.fft.fft(data)
    freqs = np.fft.fftfreq(len(fft_result), 1 / SAMPLING_RATE)
    
    # Use only the positive half of the FFT result (real frequencies)
    positive_freqs = freqs[:len(freqs) // 2]
    positive_magnitudes = np.abs(fft_result[:len(fft_result) // 2])
    
    # Identify the frequency with the maximum magnitude
    if np.max(positive_magnitudes) > 0:
        dominant_freq = positive_freqs[np.argmax(positive_magnitudes)]
    else:
        dominant_freq = 0.0
    
    print(f"Dominant Frequency: {dominant_freq:.2f} Hz")

def plot_data(samples):
    """
    Plot time-domain and frequency-domain data.
    """
    # Time domain plot
    plt.figure(figsize=(12, 6))
    
    # Time-domain subplot
    plt.subplot(2, 1, 1)
    plt.plot(samples, color='blue')
    plt.title('Time Domain Signal')
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    
    # Frequency-domain subplot
    data = np.array(samples) - np.mean(samples)  # DC offset removal
    fft_result = np.fft.fft(data)
    freqs = np.fft.fftfreq(len(fft_result), 1 / SAMPLING_RATE)
    
    positive_freqs = freqs[:len(freqs) // 2]
    positive_magnitudes = np.abs(fft_result[:len(fft_result) // 2])
    
    plt.subplot(2, 1, 2)
    plt.plot(positive_freqs, positive_magnitudes, color='red')
    plt.title('Frequency Domain Spectrum')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    
    plt.tight_layout()
    plt.show()

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
