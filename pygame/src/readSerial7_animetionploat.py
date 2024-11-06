import serial
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import threading

# Serial configuration
SERIAL_PORT = '/dev/tty.usbserial-0001'  # Adjust as needed
BAUD_RATE = 500000                       # Set to match each 8-bit transmission's baud rate
TIMEOUT = 1                               # Timeout for serial read in seconds

# FFT and Plotting configuration
SAMPLE_SIZE = 1024                        # Number of samples for FFT (adjustable)
SAMPLING_RATE = 250000                    # Effective data rate for complete 12-bit samples (Hz)

# Buffer for storing 12-bit ADC samples
sample_buffer = deque(maxlen=SAMPLE_SIZE)

def assemble_12bit_value(msb, lsb):
    """
    Combine the two 8-bit segments into a single 12-bit value.
    """
    return (msb << 4) | (lsb >> 4)

def read_uart_data():
    """
    Reads data from UART in a separate thread, filling the sample buffer.
    """
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT) as ser:
        while True:
            if ser.in_waiting >= 2:
                msb = ser.read(1)
                lsb = ser.read(1)
                
                msb = int.from_bytes(msb, byteorder='big')
                lsb = int.from_bytes(lsb, byteorder='big')
                
                adc_value = assemble_12bit_value(msb, lsb)
                
                sample_buffer.append(adc_value)  # Update buffer with latest value

def perform_fft_analysis(samples):
    """
    Perform FFT on the samples to get frequency-domain information.
    """
    if len(samples) == 0:
        return np.array([]), np.array([])  # Return empty arrays if no samples
    
    # Convert samples to numpy array and remove DC offset
    data = np.array(samples) - np.mean(samples)
    fft_result = np.fft.fft(data)
    freqs = np.fft.fftfreq(len(fft_result), 1 / SAMPLING_RATE)
    
    positive_freqs = freqs[:len(freqs) // 2]
    positive_magnitudes = np.abs(fft_result[:len(fft_result) // 2])
    print(f"Dominant Frequency: {positive_freqs:.2f} Hz")
    return positive_freqs, positive_magnitudes

def update_plot(frame, time_line, freq_line):
    """
    Update the time and frequency domain plots with the latest data.
    """
    time_data = list(sample_buffer)
    if len(time_data) < SAMPLE_SIZE:
        return time_line, freq_line
    
    # Time domain update
    time_line.set_ydata(time_data)
    
    # Perform FFT and get frequency data
    positive_freqs, positive_magnitudes = perform_fft_analysis(time_data)
    freq_line.set_data(positive_freqs, positive_magnitudes)
    
    return time_line, freq_line

def animate_plot():
    """
    Set up the real-time plotting for time and frequency domains.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))
    
    # Set up time-domain plot
    ax1.set_title("Time Domain Signal")
    ax1.set_xlabel("Sample")
    ax1.set_ylabel("Amplitude")
    time_data = np.zeros(SAMPLE_SIZE)
    time_line, = ax1.plot(time_data, color='blue')
    ax1.set_ylim(0, 4095)  # ADC 12-bit range

    # Set up frequency-domain plot
    ax2.set_title("Frequency Domain Spectrum")
    ax2.set_xlabel("Frequency (Hz)")
    ax2.set_ylabel("Magnitude")
    freq_data_x = np.fft.fftfreq(SAMPLE_SIZE, 1 / SAMPLING_RATE)[:SAMPLE_SIZE // 2]
    freq_data_y = np.zeros(SAMPLE_SIZE // 2)
    freq_line, = ax2.plot(freq_data_x, freq_data_y, color='red')
    ax2.set_xlim(0, SAMPLING_RATE // 2)
    ax2.set_ylim(0, 1000)  # Adjust based on expected magnitude range

    # Animation function update for both plots
    ani = animation.FuncAnimation(
        fig,
        update_plot,
        fargs=(time_line, freq_line),
        interval=50,
        blit=True,
        cache_frame_data=False
    )

    plt.tight_layout()
    plt.show()

# Start the data reading in a separate thread
data_thread = threading.Thread(target=read_uart_data)
data_thread.daemon = True
data_thread.start()

# Run the animated plot
animate_plot()
