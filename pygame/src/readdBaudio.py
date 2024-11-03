import pyaudio
import numpy as np

# Audio configuration
FORMAT = pyaudio.paInt16    # 16-bit resolution
CHANNELS = 1                # Mono channel
RATE = 44100                # 44.1kHz sample rate
CHUNK = 1024                # Number of frames per buffer

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Recording dB levels... Press Ctrl+C to stop.")

try:
    while True:
        # Read audio data
        data = stream.read(CHUNK, exception_on_overflow=False)

        # Convert audio data to numpy array
        audio_data = np.frombuffer(data, dtype=np.int16)

        # Compute RMS and dB
        rms = np.sqrt(np.mean(np.square(audio_data)))
        db = 20 * np.log10(rms) if rms > 0 else -float('inf')  # Avoid log(0)

        # Print the dB level
        print(f"Real-time dB Level: {db:.2f} dB")

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
