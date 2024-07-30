# Audio Processing and Noise Reduction

This repository contains code for recording, processing, and reducing noise from audio files. The code captures live audio, processes it to reduce noise, applies various audio effects, and saves the cleaned audio to a new file.

## Features

- **Audio Recording**: Captures live audio from a microphone.
- **Noise Reduction**: Uses `noisereduce` library to reduce noise from the recorded audio.
- **Audio Effects**: Applies effects such as noise gating, compression, filtering, and gain adjustment using `pedalboard`.
- **Playback and Saving**: Plays back the processed audio and saves it to a new file.

## Installation

To run the code, you need to install the following Python packages. You can install them using `pip`:

```bash
pip install pyaudio pydub ipython matplotlib sounddevice soundfile pedalboard noisereduce
