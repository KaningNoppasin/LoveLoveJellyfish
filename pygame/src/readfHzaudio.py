import pyaudio
import numpy as np

# Audio configuration
FORMAT = pyaudio.paInt16     # 16-bit resolution
CHANNELS = 1                 # Mono channel
RATE = 44100                 # 44.1kHz sample rate
CHUNK = 1024                 # Number of frames per buffer

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Recording frequencies... Press Ctrl+C to stop.")

try:
    while True:
        # Read audio data from the microphone
        data = stream.read(CHUNK, exception_on_overflow=False)

        # Convert audio data to numpy array
        audio_data = np.frombuffer(data, dtype=np.int16)

        # Apply FFT to find frequency spectrum
        fft_data = np.fft.fft(audio_data)

        # Get frequency bins
        freqs = np.fft.fftfreq(len(fft_data), 1 / RATE)

        # Calculate magnitudes and find the dominant frequency
        magnitudes = np.abs(fft_data)
        # Only consider positive frequencies
        dominant_freq = abs(freqs[np.argmax(magnitudes[:CHUNK // 2])])

        # Print the dominant frequency in real-time
        print(f"Real-time Dominant Frequency: {dominant_freq:.2f} Hz")

except KeyboardInterrupt:
    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("\nStopped recording.")

except Exception as e:
    # Handle any unexpected errors
    print(f"An error occurred: {e}")

finally:
    # Ensure the stream is closed upon exit
    stream.stop_stream()
    stream.close()
    p.terminate()
