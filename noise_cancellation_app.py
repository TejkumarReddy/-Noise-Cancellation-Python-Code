import streamlit as st
import soundfile as sf
import noisereduce as nr
from pedalboard import Pedalboard, NoiseGate, Compressor, LowShelfFilter, Gain
from pedalboard.io import AudioFile
import tempfile
import numpy as np
from pydub import AudioSegment
import io

st.set_page_config(page_title="Noise Cancellation", page_icon="🔊", layout="centered")

# Page styling with Streamlit markdown
st.markdown(
    """
    <style>
    h1 {
        color: #3949ab;
        font-family: Arial, sans-serif;
        font-weight: bold;
        text-align: center;
    }
    .section-title {
        color: #333333;
        font-weight: bold;
        font-size: 1.2em;
        border-bottom: 2px solid #3949ab;
        padding-bottom: 5px;
        margin-top: 20px;
    }
    .audio-container {
        background-color: #e1bee7;  /* Light purple container background */
        border: 2px solid #9c27b0;  /* Purple border */
        border-radius: 5px;
        padding: 10px;
        margin: 15px 0;
    }
    .button-container {
        background-color: #ffecb3;  /* Light yellow button container */
        padding: 15px;
        border-radius: 5px;
        margin-top: 15px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🔊 Noise Cancellation Tool")

# Section to Upload Audio
st.markdown('<p class="section-title">Upload an Audio File</p>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload an audio file (MP3 format only)", type=["mp3"])

audio_path = None
audio_data = None

if uploaded_file:
    # Ensure the file is an MP3
    if uploaded_file.type != "audio/mp3":
        st.error("Please upload only MP3 files.")
    else:
        # Load MP3 file with pydub
        audio = AudioSegment.from_mp3(uploaded_file)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            audio.export(temp_file.name, format="mp3")
            audio_path = temp_file.name

        st.markdown('<div class="audio-container"><strong>Noisy Audio:</strong></div>', unsafe_allow_html=True)
        st.audio(uploaded_file)

        # Process and Play the Audio
        if st.button("Generate Noiseless Audio"):
            # Read audio file
            with AudioFile(audio_path).resampled_to(44100) as f:
                audio_data = f.read(f.frames)

            # Noise reduction
            reduced_noise = nr.reduce_noise(y=audio_data, sr=44100, stationary=True, prop_decrease=0.75)

            # Apply effects
            board = Pedalboard([
                NoiseGate(threshold_db=10, ratio=2, release_ms=200),
                Compressor(threshold_db=-10, ratio=3),
                LowShelfFilter(cutoff_frequency_hz=250, gain_db=5, q=1),
                Gain(gain_db=20)
            ])
            effected_audio = board(reduced_noise, 44100)

            # Save noiseless audio in MP3 format
            noiseless_path = "noiseless_output.mp3"
            effected_audio_segment = AudioSegment(
                effected_audio[0].tobytes(),
                frame_rate=44100,
                sample_width=2,
                channels=1
            )
            effected_audio_segment.export(noiseless_path, format="mp3")

            st.success("Noiseless audio generated successfully.")
            st.markdown('<div class="audio-container"><strong>Noiseless Audio:</strong></div>', unsafe_allow_html=True)
            st.audio(noiseless_path, format="audio/mp3")

            # Download button
            with open(noiseless_path, "rb") as file:
                st.download_button(
                    label="Download Noiseless Audio",
                    data=file,
                    file_name="noiseless_output.mp3",
                    mime="audio/mp3"
                )

st.markdown('<p style="text-align: center; color: #888888;">Powered by Tej</p>', unsafe_allow_html=True)
