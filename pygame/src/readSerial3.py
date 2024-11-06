import serial
import time
import numpy as np

# Configure the serial port
ser = serial.Serial(
    port='/dev/tty.usbserial-0001',  # Replace with your serial port name
    # baudrate=115200,
    # baudrate=250000,
    baudrate=2000000,
    timeout=1
)

# Define the sampling duration and sample rate
sampling_duration = 1  # seconds
sample_rate = 1000     # Replace with your actual sample rate

try:
    while True:
        adc_values = []  # Use a list to collect ADC values
        start_time = time.time()
        
        # Collect ADC values for the defined sampling duration
        while time.time() - start_time < sampling_duration:
            if ser.in_waiting > 0:
                # Read data from UART and decode it
                data = ser.read(1)  # Read 2 bytes (assuming 12-bit data sent as two bytes)
                value = int.from_bytes(data, byteorder='little')
                adc_values.append(value)
                print("ADC Value:", value)
            time.sleep(0.01)  # Adjust for desired sampling rate
        
        # Perform FFT
        if len(adc_values) > 0:  # Ensure there are values to process
            adc_values = np.array(adc_values)  # Convert to a NumPy array
            fft_result = np.fft.fft(adc_values)

            # Compute frequencies
            N = len(adc_values)
            freq = np.fft.fftfreq(N, d=1/sample_rate)

            # Get magnitude spectrum
            magnitude = np.abs(fft_result)

            # Find the dominant frequency
            dominant_freq = abs(freq[np.argmax(magnitude[:N // 2])])  # Only consider positive frequencies
            
            # Print the dominant frequency in real-time
            print(f"Real-time Dominant Frequency: {dominant_freq:.2f} Hz")
except KeyboardInterrupt:
    print("Exiting...")
finally:
    ser.close()
