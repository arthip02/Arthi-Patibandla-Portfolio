#!/usr/bin/env python3

import argparse
import random
import numpy as np
from scipy.io import wavfile

SAMPLE_RATE = 48000
MAX_16BIT = 32767

# Song structures
SONG_STRUCTURES = [
    "AABB/CC",
    "ABAB/CD",
    "AB/CDDD"
]

# Chord loops
CHORD_LOOPS = [
    ["I", "IV", "ii", "V"],
    ["I", "vi", "ii", "V"],
    ["I", "iii", "IV", "iv"],
    ["I", "V", "ii", "V"],
    ["I", "vi", "IV", "V"],
    ["IV", "I", "vi", "IV"],
    ["I", "V", "vi", "I"],
    ["I", "IV", "iv", "I"],
    ["IV", "V", "I", "I"],
    ["vi", "IV", "I", "V"]
]

# MIDI note values
NOTE_VALUES = {
    "C": 60,
    "D": 62,
    "E": 64,
    "F": 65,
    "G": 67,
    "A": 69,
    "B": 71
}

# Major scale intervals
MAJOR_SCALE = [0, 2, 4, 5, 7, 9, 11]

# Roman numeral chord mapping
CHORD_MAP = {
    "I": [0, 2, 4],
    "ii": [1, 3, 5],
    "iii": [2, 4, 6],
    "IV": [3, 5, 0],
    "V": [4, 6, 1],
    "vi": [5, 0, 2],
    "iv": [3, 5, 0]
}


def midi_to_freq(midi_note):
    return 440.0 * (2 ** ((midi_note - 69) / 12))


def sawtooth_wave(freq, duration, amplitude=0.3):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)

    # Sawtooth wave
    wave = 2 * (t * freq - np.floor(0.5 + t * freq))

    # Fade in/out to reduce clicks
    fade_samples = 200

    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)

    wave[:fade_samples] *= fade_in
    wave[-fade_samples:] *= fade_out

    return amplitude * wave


def build_scale(root_note):
    root_midi = NOTE_VALUES[root_note]

    scale = []

    for step in MAJOR_SCALE:
        scale.append(root_midi + step)

    return scale


def chord_notes(scale, chord_name):
    degrees = CHORD_MAP[chord_name]

    notes = []

    for d in degrees:
        notes.append(scale[d % 7])

    return notes


def generate_song():

    # Random structure
    structure = random.choice(SONG_STRUCTURES)

    # Get unique labels
    labels = sorted(set(structure.replace("/", "")))

    # Assign unique chord loops
    loops = random.sample(CHORD_LOOPS, len(labels))

    label_to_loop = {}

    for i, label in enumerate(labels):
        label_to_loop[label] = loops[i]

    # Random key
    key = random.choice(["A", "B", "C", "D", "E", "F", "G"])

    # Random tempo
    tempo = random.randint(80, 160)

    beat_duration = 60 / tempo
    eighth_note_duration = beat_duration / 2

    scale = build_scale(key)

    song_audio = []

    print("Song Structure:", structure)
    print("Key:", key)
    print("Tempo:", tempo, "BPM")

    print("\nChord Loops:")
    for label in label_to_loop:
        print(label, ":", "-".join(label_to_loop[label]))

    # Build song
    for label in structure:

        if label == "/":
            continue

        loop = label_to_loop[label]

        # 4 measures per line
        for chord_name in loop:

            current_chord = chord_notes(scale, chord_name)

            # 8 eighth notes
            for _ in range(8):

                # 80% choose from chord
                if random.random() < 0.8:
                    note = random.choice(current_chord)
                else:
                    note = random.choice(scale)

                freq = midi_to_freq(note)

                wave = sawtooth_wave(freq, eighth_note_duration)

                song_audio.append(wave)

    audio = np.concatenate(song_audio)

    # Normalize
    audio = audio / np.max(np.abs(audio))

    audio = np.int16(audio * MAX_16BIT)

    return audio


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--output",
        help="Write WAV output file"
    )

    args = parser.parse_args()

    audio = generate_song()

    if args.output:

        wavfile.write(
            args.output,
            SAMPLE_RATE,
            audio
        )

        print("\nWAV file written:", args.output)

    else:
        try:
            import sounddevice as sd

            sd.play(audio, SAMPLE_RATE)
            sd.wait()

        except ImportError:
            print("\nInstall sounddevice to play audio:")
            print("pip install sounddevice")


if __name__ == "__main__":
    main()