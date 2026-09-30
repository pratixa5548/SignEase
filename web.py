import os
import time
import pygame
import cv2
import numpy as np
import streamlit as st
import speech_recognition as sr
import sounddevice as sd
import scipy.io.wavfile as wav
from io import BytesIO
from glob import glob
from gtts import gTTS
from googletrans import Translator
from cvzone.HandTrackingModule import HandDetector
import tensorflow as tf

st.set_page_config(page_title="SignEase", page_icon=":material/sign_language:", layout="wide")

# =============================== CONFIGURATION =============================== #
SIGN_MEDIA_FOLDER = "signs_webm"
MODEL_PATH = "converted_tflite/model_unquant.tflite"
LABELS_PATH = "converted_tflite/labels.txt"
source_languages = ["Tamil", "Sinhala", "Chinese", "English"]
LANGUAGE_CODES = {
    "Tamil": {"speech": "ta-IN", "translation": "ta"},
    "Sinhala": {"speech": "si-LK", "translation": "si"},
    "Chinese": {"speech": "zh-CN", "translation": "zh-cn"},
    "English": {"speech": "en-US", "translation": "en"},
}

# ============================== INITIALIZATION ============================== #
pygame.mixer.init()
translator = Translator()
_current_audio_buffer = None

# ---------------------------- Load Labels ---------------------------- #
try:
    with open(LABELS_PATH, 'r') as f:
        labels = [l.strip().split(maxsplit=1)[1] for l in f]
except FileNotFoundError:
    labels = []
    st.error("Labels file not found. Sign detection will not work.")

# ---------------------------- Load Model ----------------------------- #
try:
    interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()
    input_d = interpreter.get_input_details()
    output_d = interpreter.get_output_details()
except Exception as e:
    interpreter = None
    st.error(f"Failed to load TFLite model: {e}")

# ================================ CLASSES ================================ #
class SignPlayer:
    def __init__(self, folder=SIGN_MEDIA_FOLDER):
        self.folder = folder
        self.supported_formats = (".webm", ".mp4", ".avi", ".gif")
        self.available_signs = self._load_available_signs()
        self.phrases = {
            "how are you": "howareyou",
            "thank you": "thankyou",
            "good morning": "goodmorning",
            "how are you": "howareyou",
            "thank you": "thankyou",
            "good morning": "goodmorning",
            "where are you going": "whereareyougoing"
        }

    def _load_available_signs(self):
        signs = []
        for ext in self.supported_formats:
            signs.extend([os.path.splitext(os.path.basename(f))[0] for f in glob(os.path.join(self.folder, f"*{ext}"))])
        return set(signs)

    def get_media_path(self, word):
        sanitized_word = word.strip().lower().replace(" ", "")
        for ext in self.supported_formats:
            path = os.path.join(self.folder, f"{sanitized_word}{ext}")
            if os.path.exists(path):
                return path
        return None

    def suggest_signs(self, word):
        word = word.lower()
        return [sign for sign in self.available_signs if word in sign or sign.startswith(word)][:3]

    def process_input(self, text_input):
        text_input = text_input.strip().lower()

        # 1. Check mapped phrases
        for phrase, combined in self.phrases.items():
            if text_input == phrase:
                path = self.get_media_path(combined)
                return [path] if path else []

        # 2. Try full phrase as single word: "howareyou"
        merged = text_input.replace(" ", "")
        merged_path = self.get_media_path(merged)
        if merged_path:
            return [merged_path]

        # 3. Fall back to word-by-word
        words = text_input.split()
        return [self.get_media_path(word) for word in words]

# ============================= FUNCTIONALITY ============================= #
def speech_to_text(from_language):
    recognizer = sr.Recognizer()
    sample_rate = 44100
    duration = 5
    st.write("Listening...")
    audio_data = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=1, dtype=np.int16)
    sd.wait()
    wav.write("temp_audio.wav", sample_rate, audio_data)
    with sr.AudioFile("temp_audio.wav") as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(
            audio, language=LANGUAGE_CODES[from_language]["speech"]
        )
    except sr.UnknownValueError:
        return "Sorry, could not understand the audio."
    except sr.RequestError:
        return "Network error. Please try again."

def translate_text(text, src_lang):
    try:
        return translator.translate(
            text, src=LANGUAGE_CODES[src_lang]["translation"], dest="en"
        ).text
    except Exception as e:
        return f"Translation Error: {str(e)}"

def text_to_speech(text):
    global _current_audio_buffer

    pygame.mixer.music.stop()
    try:
        pygame.mixer.music.unload()
    except pygame.error:
        pass

    audio_buffer = BytesIO()
    gTTS(text=text, lang="en", slow=False).write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    pygame.mixer.music.load(audio_buffer, namehint="mp3")
    _current_audio_buffer = audio_buffer
    pygame.mixer.music.play()

def play_sign_video(video_paths, playback_speed=1.0):
    if not video_paths or all(not os.path.exists(p) for p in video_paths if p):
        missing_words = [w for w, p in zip(st.session_state.get('current_words', []), video_paths) if not p]
        st.error(f"No signs found for: {', '.join(missing_words)}")
        for word in missing_words:
            suggestions = st.session_state.player.suggest_signs(word)
            if suggestions:
                st.info(f"For '{word}', did you mean: {', '.join(suggestions)}?")
        return
    video_placeholder = st.empty()
    for video_path in filter(None, video_paths):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened(): continue
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            video_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), width="stretch")
            time.sleep(1 / (30 * playback_speed))
        cap.release()

# =========================== STREAMLIT UI LAUNCH ============================ #
from ui_main import render_ui
render_ui(
    source_languages=source_languages,
    SignPlayer=SignPlayer,
    speech_to_text=speech_to_text,
    translate_text=translate_text,
    text_to_speech=text_to_speech,
    play_sign_video=play_sign_video,
    interpreter=interpreter,
    input_d=input_d if interpreter else None,
    output_d=output_d if interpreter else None,
    labels=labels
)