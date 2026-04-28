import numpy as np
from scipy.io import wavfile

# Read WAV file
fs, data = wavfile.read("message.wav")

# Convert to mono if needed
if len(data.shape) > 1:
    data = data[:, 0]

# Convert to float in range [-1, 1]
data = data.astype(np.float32) / 32768.0

BIT_SIZE = 160  # 48000 / 300 baud 


def tone_power(samples, f, fs):
    N = len(samples)
    n = np.arange(N)
    cos_ref = np.cos(2 * np.pi * f * n / fs)
    sin_ref = np.sin(2 * np.pi * f * n / fs)

    I = np.dot(samples, cos_ref)
    Q = np.dot(samples, sin_ref)

    return I**2 + Q**2


# Decode one bit per 160-sample block
bits = []
for i in range(0, len(data), BIT_SIZE):
    block = data[i:i + BIT_SIZE]
    if len(block) < BIT_SIZE:
        break

    p0 = tone_power(block, 2025, fs)  # bit 0
    p1 = tone_power(block, 2225, fs)  # bit 1

    bit = 1 if p1 > p0 else 0
    bits.append(bit)

# Group bits into 10-bit frames: 1 start, 8 data, 1 stop
bytes_out = []
for i in range(0, len(bits), 10):
    frame = bits[i:i + 10]
    if len(frame) < 10:
        break

    start = frame[0]
    data_bits = frame[1:9]
    stop = frame[9]

    # Optional framing check
    if start != 0 or stop != 1:
        print(f"Warning: framing error in frame {i//10}: start={start}, stop={stop}")

    # LSB-first byte assembly
    value = 0
    for j, b in enumerate(data_bits):
        value |= (b << j)

    bytes_out.append(value)

# Convert bytes to text
text = ''.join(chr(b) for b in bytes_out)

print("Decoded message:")
print(text)

# Save output
with open("message.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("\nSaved decoded message to message.txt")