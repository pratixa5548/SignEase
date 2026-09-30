import os
import pygame
import streamlit as st
import speech_recognition as sr
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
from gtts import gTTS
from googletrans import Translator  # Ensure this is the library import

# Initialize pygame for text-to-speech playback
pygame.mixer.init()
translator = Translator()

# 🔹 Available source languages (Only translating to English)
source_languages = ["Tamil", "Sinhala", "Chinese", "English"]

# 🔹 Streamlit UI
st.title("Speech-to-English Translator")

col1, col2 = st.columns(2)
with col1:
    from_language = st.selectbox("From Language", source_languages)
with col2:
    to_language = "English"  # Fixed target language

# 🔹 Session State Initialization
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""
if "audio_ready" not in st.session_state:
    st.session_state.audio_ready = False  # Flag to control audio playback
if "input_mode" not in st.session_state:
    st.session_state.input_mode = None  # Determines whether speech or text is active

# 🔹 Two Separate Text Areas for Input and Output
st.session_state.input_text = st.text_area("Input Text (Speech/Text):", st.session_state.input_text)
st.text_area("Translated Output:", st.session_state.translated_text, key="output_text_display")

# 🔹 Speech-to-Text Function
def speech_to_text():
    recognizer = sr.Recognizer()
    
    # Set recording parameters
    sample_rate = 44100  # CD-quality audio
    duration = 5  # Record for 5 seconds

    # Capture audio
    st.write("Listening...")
    audio_data = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=1, dtype=np.int16)
    sd.wait()  # Wait until recording is finished

    # Save recorded audio to a temporary file
    temp_audio_file = "temp_audio.wav"
    wav.write(temp_audio_file, sample_rate, audio_data)

    with sr.AudioFile(temp_audio_file) as source:
        audio = recognizer.record(source)  # Read the entire file

    # Convert speech to text
    try:
        text = recognizer.recognize_google(audio, language=from_language.lower()[:2])
        return text
    except sr.UnknownValueError:
        return "Sorry, could not understand the audio."
    except sr.RequestError:
        return "Network error. Please try again."

# 🔹 Translation Function
def translate_text(text, src_lang):
    try:
        translated = translator.translate(text, src=src_lang.lower()[:2], dest="en")
        return translated.text
    except Exception as e:
        return f"Translation Error: {str(e)}"

# 🔹 Text-to-Speech Function (Plays After Clicking Translate)
def text_to_speech(text):
    audio_file = "translated_audio.mp3"

    # Release pygame mixer if it's already playing
    pygame.mixer.quit()
    pygame.mixer.init()

    # Delete existing file to avoid permission errors
    if os.path.exists(audio_file):
        os.remove(audio_file)

    # Generate new speech file
    tts = gTTS(text=text, lang="en", slow=False)
    tts.save(audio_file)

    # Play the audio
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

# 🔹 Input Selection Buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Start Speech Input"):
        st.session_state.input_mode = "speech"
        spoken_text = speech_to_text()
        st.session_state.input_text = spoken_text  # Store speech input in input box

# Removed "Start Text Input" button and its logic

if st.button("Translate"):  
    if st.session_state.input_text.strip():  # Check if input exists
        translated_text = translate_text(st.session_state.input_text, from_language)
        
        # Update session state **before playing audio**
        st.session_state.translated_text = translated_text  
        st.session_state.audio_ready = True  # Mark audio as ready

        # Immediately display the translation and play audio
        st.rerun()

    else:
        st.warning("Please enter or speak text first.")

# 🔹 Play audio **only after Translate is clicked**
if st.session_state.audio_ready:
    text_to_speech(st.session_state.translated_text)
    st.session_state.audio_ready = False  # Reset audio flag

# 🔹 Reset Button
if st.button("Reset"):
    st.session_state.input_text = ""  # Clear input
    st.session_state.translated_text = ""  # Clear output
    st.session_state.input_mode = None  # Reset input mode
    st.session_state.audio_ready = False  # Reset audio flag
    st.rerun()