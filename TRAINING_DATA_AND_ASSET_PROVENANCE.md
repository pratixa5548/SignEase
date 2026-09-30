# SignEase: Training Data and Asset Provenance

This document explains the origin of the data, models, and media used by SignEase.

Its purpose is to make it clear which parts of the project were created by the project team and which parts use external services or third-party software.

> **Important:** This document only states information supported by the available project records. It does not assign a dataset name, license, model architecture, dataset size, or performance result where those details cannot be verified.

---

## 1. At a Glance

| Component             | Source                                                                       |
| --------------------- | ---------------------------------------------------------------------------- |
| Webcam training data  | Collected by the project team                                                |
| Gesture preprocessing | Project-collected data processed using computer-vision/data-processing tools |
| Webcam classifier     | Trained as part of the project                                               |
| Deployed model        | TensorFlow Lite conversion of the trained classifier                         |
| Text-to-sign videos   | Recorded by the project team using a Rylo camera                             |
| Sign/phrase mappings  | Developed as part of the application                                         |
| Speech recognition    | External Google service                                                      |
| Translation           | Google Translate                                                             |
| Text-to-speech        | Google Text-to-Speech / `gTTS`                                               |

---

# 2. Webcam Sign-Recognition Data

## Source of the data

The raw gesture data used to train the webcam sign-recognition classifier was **collected by the project team**.

The team captured multiple examples of the supported hand signs.

The training data was therefore created from project-collected gesture samples rather than being taken wholesale from a single publicly available sign-language dataset.

No specific public dataset is being claimed as the source of this training data.

---

## Data collection

Multiple samples were captured for the gestures that the project intended the classifier to recognize.

The purpose of collecting multiple examples was to provide variation in the captured gestures and images.

The current deployment repository does not contain the original collection archive, so the exact number of images/samples collected for each class is not documented here.

For that reason, this document intentionally does not claim a specific dataset size.

---

## Data preparation

After collection, the gesture data was combined, organized, cleaned, and processed using various data-processing and computer-vision tools.

The overall development process can be represented as:

```text
Gesture examples captured by project team
                    ↓
             Data collection
                    ↓
          Data organization
                    ↓
            Data cleaning
                    ↓
     Computer-vision processing
                    ↓
       Training-data preparation
                    ↓
             Model training
                    ↓
       TensorFlow Lite conversion
                    ↓
             App inference
```

The complete original preprocessing scripts are not included in the current GitHub repository.

Therefore, this document does not claim specific preprocessing algorithms beyond what can be established from the available project materials.

---

# 3. Webcam Model

The trained gesture classifier was converted to TensorFlow Lite for use in the application.

The deployed files are:

```text
converted_tflite/model_unquant.tflite
converted_tflite/labels.txt
```

`labels.txt` contains the classes supported by the deployed model.

The model has a limited vocabulary of approximately ten classes. Examples include:

* hello
* you
* ok
* thank you
* i love you
* good
* no
* bye
* please
* sorry

The actual current class list should always be taken from `converted_tflite/labels.txt`.

The model should therefore be described as a **limited-vocabulary gesture classifier**, not as a complete ISL recognition model.

---

# 4. Computer-Vision Processing

The deployed application uses computer-vision processing to locate the hand before sending it to the classifier.

The application uses tools including **cvzone and MediaPipe** for hand detection.

During inference, the detected hand region is processed before classification. The current application performs steps including:

1. Hand detection
2. Cropping
3. Padding where required
4. Resizing to `224 × 224`
5. Normalization
6. TensorFlow Lite inference
7. Mapping the output to the corresponding label

These steps describe the deployed application pipeline.

They should not be treated as a complete reconstruction of every step used during the original training process.

---

# 5. Sign-Video Assets

The project also contains a collection of pre-recorded sign-language videos in:

```text
signs_webm/
```

These videos were **recorded by the project team using a Rylo camera**.

They were created for selected words and expressions needed by the project.

They are therefore project-created video assets rather than a downloaded public sign-language video dataset.

The application uses them through word and phrase mappings.

For example:

```text
Entered text
     ↓
Phrase / word mapping
     ↓
Matching local video
     ↓
Video playback
```

If a complete phrase video is unavailable, the application can fall back to available word-level clips according to its mapping logic.

---

# 6. What the Sign Videos Are Not

The sign videos are not:

* a complete ISL dataset;
* a complete ISL vocabulary;
* a neural sign-generation model;
* automatically generated videos;
* a model capable of producing arbitrary signs from text.

They are a limited set of recordings made specifically for the project.

---

# 7. External Services

Several parts of SignEase use existing external services.

## Speech recognition

The application records a short audio sample and sends it to the configured Google speech-recognition service.

The SignEase team did not train the underlying speech-recognition model.

## Translation

Text translation is performed using **Google Translate**.

The SignEase team did not train the translation model.

## Text-to-speech

English text is converted to speech using **Google Text-to-Speech (`gTTS`)**.

The SignEase team did not train the underlying text-to-speech model.

These services are external dependencies and are subject to their own terms and policies.

---

# 8. What Was Developed or Trained by the Project

The following parts were developed as part of SignEase:

### Webcam gesture classifier

The project team:

* collected the gesture examples;
* prepared the collected data;
* trained the classifier;
* converted the resulting model to TensorFlow Lite; and
* integrated the model into the application.

### Sign-video library

The project team:

* recorded the sign videos using a Rylo camera; and
* integrated the recordings into the text-to-sign functionality.

### Application

The project team also developed the application logic connecting speech, translation, text-to-sign playback, and webcam recognition.

---

# 9. What Was Not Trained by the Project

The following were **not** trained by the SignEase team:

* Google's speech-recognition model;
* Google Translate;
* Google Text-to-Speech;
* TensorFlow Lite itself;
* MediaPipe;
* cvzone;
* other third-party libraries used by the application.

The project uses these technologies as external software/services.

---

# 10. What Is Included in This Repository?

The current GitHub repository is primarily a **deployment/demo repository**.

It includes the files needed to run the application and use the deployed model, including:

```text
converted_tflite/model_unquant.tflite
converted_tflite/labels.txt
signs_webm/
```

The repository does **not** contain the complete original:

* raw gesture dataset;
* original data-collection archive;
* training notebooks;
* model-training scripts;
* training configuration/history; or
* complete original preprocessing pipeline.

The trained TensorFlow Lite model is included, but the original training environment is not fully archived here.

---

# 11. Reproducibility

Because the original raw training data and complete training pipeline are not included, cloning this repository does not reproduce the original model-training experiment from scratch.

It does, however, provide the trained TensorFlow Lite model required for running webcam inference in the application.

In other words:

```text
Original project
      ↓
Project team collected gesture data
      ↓
Data preparation and training
      ↓
Trained classifier
      ↓
TensorFlow Lite conversion
      ↓
Current GitHub repository
      ↓
Inference / demonstration
```

This repository should therefore be understood as the **deployed application and model**, rather than a complete archive of the original research/training environment.

---

# 12. Dataset and Licensing Information

Because the webcam training data was collected by the project team, this repository does not identify it as a particular public dataset.

No third-party dataset license is being claimed for the project-collected gesture data.

Similarly, the project-recorded sign videos are not being attributed to an external dataset.

This documentation does **not** grant additional rights to any third-party software, service, image, video, or other material included in or used by the project.

---

# 13. Copyright and Redistribution

The project team created the gesture samples and sign-video recordings described in this document.

However, the complete repository may also contain or depend on third-party material.

Before redistributing the repository, verify the applicable rights for each third-party asset.

In particular:

* Retain required third-party attribution.
* Do not remove copyright or license notices.
* Do not assume that material found online is free to redistribute.
* Check the license or permission for every third-party image or media file.
* Check the applicable terms for external APIs and services.
* Do not apply the project's own license to third-party material unless the project team has the right to do so.

This provenance document records where the project data and assets came from; it does not itself grant permission to redistribute third-party material.

---

# 14. Interface Image Sources

The application README currently identifies these interface images:

### Speech translator

Artem Podrez via Pexels:

https://www.pexels.com/photo/woman-sitting-on-a-wooden-chair-with-earpods-waving-on-a-video-call-8512149/

### Text-to-sign

Myblueberet via Wikimedia Commons, identified as CC BY-SA 4.0:

https://commons.wikimedia.org/wiki/File:Sign_language_communicator.jpg

### Sign detector

Mary Mark Ockerbloom via Wikimedia Commons, identified as CC0:

https://commons.wikimedia.org/wiki/File:Signer_James_Rowe_2014-12-07_DSCF0926_crop.jpg

These sources and their stated licenses should be checked against the actual files in the repository before redistribution.

---

# 15. Recommended Description of the Project

For CVs, GitHub descriptions, reports, or project documentation, the most accurate short description is:

> **SignEase is a limited-vocabulary multimodal prototype combining speech recognition, Google Translate, text-to-speech, pre-recorded sign-language video playback, and webcam-based gesture recognition. The webcam classifier was trained using gesture data collected and processed by the project team and deployed as a TensorFlow Lite model. The sign-video component uses project-recorded videos for selected words and expressions.**

---

# 16. Provenance Summary

| Item                                              | Provenance                              |
| ------------------------------------------------- | --------------------------------------- |
| Raw webcam gesture samples                        | Collected by project team               |
| Training data                                     | Prepared from project-collected samples |
| Gesture classifier                                | Trained as part of project              |
| TensorFlow Lite model                             | Converted deployment model              |
| Sign videos                                       | Recorded by project team using Rylo     |
| Sign/phrase mappings                              | Developed for project                   |
| Speech recognition                                | External Google service                 |
| Translation                                       | Google Translate                        |
| Text-to-speech                                    | Google Text-to-Speech / `gTTS`          |
| Complete raw training dataset in repository       | No                                      |
| Complete original training pipeline in repository | No                                      |
| Complete ISL vocabulary                           | No                                      |
| Arbitrary neural sign-video generation            | No                                      |

---

## Final Note

The key provenance distinction is:

**The project's own machine-learning data was collected by the project team, and the project's sign videos were recorded by the project team. Google services provide speech recognition, translation, and text-to-speech.**

The current repository contains the deployed application, trained TensorFlow Lite model, and sign-video assets, but not the complete original training dataset or training pipeline.
