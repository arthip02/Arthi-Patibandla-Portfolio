import numpy as np
from scipy.io.wavfile import write
import sounddevice as sd
import matplotlib.pyplot as plt

SAMPLE_RATE = 48000
DURATION = 1.0
FREQUENCY = 440
MAX_16BIT = 32767

SINE_AMPLITUDE = 8192
CLIPPED_SOURCE_AMPLITUDE = 16384
CLIP_MIN = -8192
CLIP_MAX = 8192


def generate_sine_wave(amplitude, frequency, duration, sample_rate):
    t = np.arange(int(sample_rate * duration)) / sample_rate
    return amplitude * np.sin(2 * np.pi * frequency * t)


def generate_clipped_sine_wave():
    raw_wave = generate_sine_wave(
        CLIPPED_SOURCE_AMPLITUDE,
        FREQUENCY,
        DURATION,
        SAMPLE_RATE
    )
    return np.clip(raw_wave, CLIP_MIN, CLIP_MAX)


def save_wav(filename, samples):
    write(filename, SAMPLE_RATE, np.int16(np.round(samples)))


def play_audio(samples):
    samples_float32 = np.array(samples / MAX_16BIT, dtype=np.float32)
    sd.play(samples_float32, SAMPLE_RATE)
    sd.wait()


def show_wave(samples, sample_rate, title, figure_num):
    n = 1000
    t = np.arange(n) / sample_rate
    samples_norm = samples / MAX_16BIT

    plt.figure(figure_num, figsize=(10, 4))
    plt.plot(t, samples_norm[:n])
    plt.title(title)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude (normalized)")
    plt.ylim(-1, 1)
    plt.grid(True)


def main():
    sine_wave = generate_sine_wave(
        SINE_AMPLITUDE,
        FREQUENCY,
        DURATION,
        SAMPLE_RATE
    )
    save_wav("sine.wav", sine_wave)

    clipped_wave = generate_clipped_sine_wave()
    save_wav("clipped.wav", clipped_wave)

    play_audio(clipped_wave)

    show_wave(sine_wave, SAMPLE_RATE, "Normal Sine Wave", 1)
    show_wave(clipped_wave, SAMPLE_RATE, "Clipped Sine Wave", 2)
    plt.show()

    print("Done!")
    print("Created: sine.wav")
    print("Created: clipped.wav")
    print("Played: clipped sine wave")


if __name__ == "__main__":
    main()