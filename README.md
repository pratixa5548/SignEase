# SignEase

SignEase is a Streamlit application for speech translation, sign-video playback, and webcam sign recognition.

## Features

- Record or type Tamil, Sinhala, Chinese, or English and translate it into English.
- Listen to the English translation with text-to-speech.
- Play available sign-language clips for entered words and phrases.
- Use the webcam to classify hand poses supported by the included TensorFlow Lite model.

## Requirements

- 64-bit Python 3.10
- A microphone for speech input
- A webcam for sign detection
- An internet connection for speech recognition, translation, and text-to-speech

## Run on Windows

From the project folder in PowerShell:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run web.py
```

Open the local URL printed by Streamlit, usually `http://localhost:8501`.

`web.py` starts the full SignEase app. `app.py` is a separate, simpler speech-to-English translator:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## Project assets

The full app expects these paths to remain in the project:

- `converted_tflite/model_unquant.tflite` and `converted_tflite/labels.txt` for sign detection
- `signs_webm/` for the sign-video library

The sign detector only recognizes classes present in `labels.txt`; text-to-sign playback only has clips for words and phrases present in `signs_webm/`.

## Audio and privacy

Speech input records a five-second microphone sample and sends it to Google's speech-recognition service. Translation and generated speech also use online services. The speech-recognition sample is written locally as `temp_audio.wav`; do not commit it or record sensitive speech when using this demo.

## Image credits

- Speech translator photo: Artem Podrez via [Pexels](https://www.pexels.com/photo/woman-sitting-on-a-wooden-chair-with-earpods-waving-on-a-video-call-8512149/).
- Text-to-sign photo: Myblueberet via [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Sign_language_communicator.jpg), CC BY-SA 4.0.
- Sign detector photo: Mary Mark Ockerbloom via [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Signer_James_Rowe_2014-12-07_DSCF0926_crop.jpg), CC0.

Before redistributing the sign-video clips or model, verify that their original licenses permit it and retain any required attribution.

