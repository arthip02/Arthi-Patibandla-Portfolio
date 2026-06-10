import math
import threading
import numpy as np
import sounddevice as sd
import mido

SAMPLE_RATE = 48000
BLOCK_SIZE = 256
ATTACK_TIME = 0.010
RELEASE_TIME = 0.010
MIDI_PORT = "synth-port 0"

current_note = None
frequency = 440.0
phase = 0.0
amplitude = 0.0
target_amplitude = 0.0
velocity_gain = 0.7

lock = threading.Lock()


def midi_note_to_freq(note):
    return 440.0 * (2 ** ((note - 69) / 12))


def audio_callback(outdata, frames, time, status):
    global phase, amplitude

    if status:
        print(status)

    audio = np.zeros(frames, dtype=np.float32)

    with lock:
        freq = frequency
        target = target_amplitude
        gain = velocity_gain

    attack_step = 1.0 / (ATTACK_TIME * SAMPLE_RATE)
    release_step = 1.0 / (RELEASE_TIME * SAMPLE_RATE)

    for i in range(frames):
        if amplitude < target:
            amplitude = min(target, amplitude + attack_step)
        elif amplitude > target:
            amplitude = max(target, amplitude - release_step)

        phase += freq / SAMPLE_RATE
        phase = phase % 1.0

        saw = 2.0 * phase - 1.0
        audio[i] = saw * amplitude * gain

    outdata[:, 0] = audio


def midi_listener():
    global current_note, frequency, target_amplitude, velocity_gain

    print(f"Listening for MIDI on: {MIDI_PORT}")
    print("Press keys in VMPK. Press Ctrl+C in PowerShell to stop.")

    with mido.open_input(MIDI_PORT) as port:
        for msg in port:
            if msg.type == "note_on" and msg.velocity > 0:
                with lock:
                    current_note = msg.note
                    frequency = midi_note_to_freq(msg.note)
                    velocity_gain = msg.velocity / 127
                    target_amplitude = 1.0
                print(f"KEY ON  note={msg.note} freq={frequency:.2f} velocity={msg.velocity}")

            elif msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0):
                with lock:
                    if current_note == msg.note:
                        target_amplitude = 0.0
                        current_note = None
                print(f"KEY OFF note={msg.note}")


def main():
    midi_thread = threading.Thread(target=midi_listener, daemon=True)
    midi_thread.start()

    with sd.OutputStream(
        samplerate=SAMPLE_RATE,
        blocksize=BLOCK_SIZE,
        channels=1,
        dtype="float32",
        callback=audio_callback,
        latency="low",
    ):
        while True:
            sd.sleep(100)


if __name__ == "__main__":
    main()