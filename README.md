# SignEase

SignEase is a Streamlit-based prototype that combines speech translation, text-to-sign video playback, and webcam-based sign recognition.

The project has three main interaction paths:

* **Speech → English text → spoken English**
* **Text → pre-recorded sign-language video**
* **Webcam → sign classification**

> **Note:** SignEase uses a limited vocabulary. It is a prototype and is **not a complete Indian Sign Language (ISL) translation or recognition system**.

For information about the origin of the training data, sign videos, and trained model, see [TRAINING_DATA_AND_ASSET_PROVENANCE.md](TRAINING_DATA_AND_ASSET_PROVENANCE.md).

---

## Features

* Record speech in supported languages and convert it to text.
* Translate recognized or typed text into English using Google Translate.
* Convert the English result to speech.
* Play available sign-language videos for supported words and phrases.
* Use a webcam to recognize the limited set of hand signs supported by the included TensorFlow Lite model.

---

## Requirements

### Software

* 64-bit Python 3.10
* Dependencies listed in `requirements.txt`
* A Windows, Linux, or macOS environment capable of running the dependencies

### Hardware

* Microphone for speech input
* Webcam for sign recognition

### Internet

An internet connection is required for the external speech-recognition, translation, and text-to-speech services.

The webcam sign-recognition inference itself runs using the model included in the repository.

---

## Installation

### Windows

Open PowerShell in the project directory and run:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Start the full application with:

```powershell
.\.venv\Scripts\python.exe -m streamlit run web.py
```

Streamlit will display a local address, normally:

```text
http://localhost:8501
```

Open that address in a browser.

### Other operating systems

Create a Python 3.10 virtual environment, install the dependencies from `requirements.txt`, and run:

```bash
python -m streamlit run web.py
```

---

## Which file should I run?

### `web.py`

This is the **main SignEase application**.

Run this to use the complete application.

### `app.py`

This is an older, simpler speech-to-English translator included in the repository.

It is separate from the full SignEase application.

To run it:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

---

## Required Project Files

The main application expects the following files/directories:

```text
converted_tflite/
├── model_unquant.tflite
└── labels.txt

signs_webm/
```

### `converted_tflite/model_unquant.tflite`

The trained TensorFlow Lite model used for webcam sign recognition.

### `converted_tflite/labels.txt`

The class labels corresponding to the model.

The model can only recognize the classes listed in this file.

### `signs_webm/`

The local library of pre-recorded sign-language videos used by the text-to-sign component.

---

# How SignEase Works

## 1. Speech Input

The application records a five-second microphone sample.

The recording is temporarily saved as:

```text
temp_audio.wav
```

Speech recognition is performed using Google's speech-recognition service.

The current application supports input including:

* English
* Tamil
* Sinhala
* Chinese

The exact language options available should be checked in the current application code.

---

## 2. Translation

Recognized speech or manually entered text can be translated into English using **Google Translate**.

SignEase does not contain its own machine-translation model.

An internet connection is therefore required.

---

## 3. Text-to-Speech

The English result can be converted into spoken audio using **Google Text-to-Speech (`gTTS`)**.

This is an external service and is not a model trained as part of SignEase.

---

## 4. Text-to-Sign

SignEase does not generate sign-language videos dynamically.

Instead, it uses **pre-recorded sign videos created by the project team** for a limited set of words and expressions.

The videos are stored in:

```text
signs_webm/
```

The application:

```text
Entered text
     ↓
Phrase / word matching
     ↓
Find available local sign clip
     ↓
Play sign video
```

If a complete phrase clip is unavailable, the application can use available word-level clips according to its mapping logic.

Therefore, text-to-sign output is limited to the words and phrases for which videos are available.

---

## 5. Webcam Sign Recognition

The webcam feed is processed to identify the user's hand and classify the supported gesture.

The deployed model is:

```text
converted_tflite/model_unquant.tflite
```

The application uses computer-vision tools including **cvzone and MediaPipe** for hand detection.

The detected hand region is prepared for the classifier and passed to the TensorFlow Lite model.

The deployed inference pipeline includes:

1. Detect the hand.
2. Crop the relevant hand region.
3. Apply required padding.
4. Resize the input to `224 × 224`.
5. Normalize the image.
6. Run TensorFlow Lite inference.
7. Map the prediction to `labels.txt`.
8. Display the predicted class and confidence.

The model has a small, predefined vocabulary. Examples include:

```text
hello
you
ok
thank you
i love you
good
no
bye
please
sorry
```

The definitive list is the one in:

```text
converted_tflite/labels.txt
```

---

# Training Data

The webcam sign-recognition model was trained using **gesture data collected by the project team**.

The team captured multiple examples of the supported gestures and prepared the collected data using various computer-vision and data-processing tools before training the classifier.

The broad process was:

```text
Project team captures gesture examples
                ↓
        Data collection
                ↓
      Data organization
                ↓
       Cleaning / processing
                ↓
   Computer-vision preprocessing
                ↓
         Model training
                ↓
     TensorFlow Lite conversion
                ↓
        Application inference
```

The original raw training data and complete training scripts are not included in this deployment repository.

For the full provenance description, see:

[TRAINING_DATA_AND_ASSET_PROVENANCE.md](TRAINING_DATA_AND_ASSET_PROVENANCE.md)

---

# Sign-Video Assets

The sign-language videos in `signs_webm/` were **recorded by the project team using a Rylo camera**.

They were created for selected words and expressions required by the project.

They are ordinary pre-recorded video assets. The application does not generate these videos using a neural network.

Because the collection is limited, the application cannot provide a sign video for arbitrary text.

---

# Important Scope

SignEase should be understood as a **limited-vocabulary prototype**.

It should not be described as:

* a complete ISL vocabulary;
* a complete ISL translation system;
* unrestricted sign-language recognition;
* a system capable of generating arbitrary sign-language videos; or
* a model trained on a named public ISL dataset unless supporting records explicitly establish that.

The webcam model recognizes only the classes in `labels.txt`.

The text-to-sign component can only play videos available in `signs_webm/`.

---

# Privacy and Runtime Audio

The speech-recognition recording is temporarily saved as:

```text
temp_audio.wav
```

This is runtime data. It is **not part of the machine-learning training data** and should not be committed to Git.

Speech is sent to an external speech-recognition service. Translation and text-to-speech also use external online services.

Avoid recording sensitive or confidential information when using the application.

---

# Image Credits

The following interface images are used in the application:

* **Speech translator:** Artem Podrez via Pexels
  https://www.pexels.com/photo/woman-sitting-on-a-wooden-chair-with-earpods-waving-on-a-video-call-8512149/

* **Text-to-sign:** Myblueberet via Wikimedia Commons, CC BY-SA 4.0
  https://commons.wikimedia.org/wiki/File:Sign_language_communicator.jpg

* **Sign detector:** Mary Mark Ockerbloom via Wikimedia Commons, CC0
  https://commons.wikimedia.org/wiki/File:Signer_James_Rowe_2014-12-07_DSCF0926_crop.jpg

The corresponding license and attribution requirements should be retained when applicable.

---

# Third-Party Services and Libraries

SignEase uses third-party software and services, including packages listed in `requirements.txt`, computer-vision libraries, TensorFlow Lite, and external Google services.

Their respective licenses and terms apply independently of this project.

The SignEase project does not claim ownership of third-party software, services, trademarks, or externally provided models.

---

# License

No open-source license is asserted for this repository unless a separate `LICENSE` file is included.

A repository license should only be applied to material for which the project team has the necessary rights.

Third-party material remains subject to its own license or permission.

---

## Further Information

For a concise record of:

* where the webcam training data came from;
* how it was prepared;
* where the sign videos came from;
* which components were trained by the project;
* which components are external services; and
* what is and is not included in this repository,

see [TRAINING_DATA_AND_ASSET_PROVENANCE.md](TRAINING_DATA_AND_ASSET_PROVENANCE.md).
