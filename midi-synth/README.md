# MIDI Sawtooth Synthesizer

Name: Arthi Patibandla
psu ID: 934131978

## Project Overview

This project implements a real-time monophonic MIDI synthesizer in Python.

The synthesizer:

- Receives MIDI input from a virtual MIDI keyboard (VMPK)
- Uses loopMIDI as a virtual MIDI connection
- Detects MIDI Note On and Note Off events
- Converts MIDI note numbers into frequencies
- Generates a sawtooth waveform
- Outputs audio through the computer speakers
- Implements a 10 ms Attack and 10 ms Release envelope

---

## Features

- Monophonic synthesis
- Sawtooth oscillator
- MIDI Note On support
- MIDI Note Off support
- Handles Note On with velocity 0 as Note Off
- Low-latency audio playback
- 10 ms Attack envelope
- 10 ms Release envelope

---

## Software Requirements

### Python

- Python 3.12

### Python Libraries

Install dependencies using:

```bash
py -3.12 -m pip install -r requirements.txt
```

Required packages:

- numpy
- sounddevice
- mido
- python-rtmidi

### External Applications

- loopMIDI
- VMPK (Virtual MIDI Piano Keyboard)

---

## Project Structure

```text
midi-synth/
├── synth.py
├── midi_test.py
├── midi_listener.py
├── requirements.txt
├── README.md
└── SYNTH.mp4
```

### File Descriptions

#### synth.py

Main synthesizer implementation.

Responsibilities:

- MIDI input handling
- Frequency calculation
- Sawtooth waveform generation
- Attack/Release envelope
- Audio playback

#### midi_test.py

Lists available MIDI input ports.

Used to verify MIDI device detection.

#### midi_listener.py

Displays incoming MIDI messages.

Used to verify Note On and Note Off events.

#### requirements.txt

Contains required Python dependencies.

---

## Setup Instructions

### Step 1 — Configure loopMIDI

Open loopMIDI.

Create a port named:

```text
synth-port
```

Keep loopMIDI running.

---

### Step 2 — Configure VMPK

Open VMPK.

Navigate to:

```text
Edit → MIDI Connections
```

Set:

```text
Output MIDI Connection = synth-port
```

Click OK.

---

## Running the Synthesizer

Open a terminal inside the project folder and run:

```bash
py -3.12 synth.py
```

Expected output:

```text
Listening for MIDI on: synth-port 0
Press keys in VMPK. Press Ctrl+C in PowerShell to stop.
```

Press keys in VMPK to generate sound.

---

## Controls

### Play Notes

Click keys inside VMPK.

Each MIDI note is converted into a frequency and played through the speakers.

### Stop the Program

Press:

```text
Ctrl + C
```

---

## Waveform

The synthesizer generates a sawtooth waveform.

MIDI note numbers are converted to frequencies using the standard MIDI frequency formula.

---

## Demo Video

A demonstration video is included as:

```text
SYNTH.mp4
```

The video demonstrates:

- loopMIDI setup
- VMPK MIDI input
- Synthesizer execution
- Note On / Note Off detection
- Real-time sound generation

---

## Conclusion

This project demonstrates the fundamentals of MIDI event handling, digital sound synthesis, waveform generation, envelope control, and real-time audio playback using Python.
