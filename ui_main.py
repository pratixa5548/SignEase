import streamlit as st
import cv2
import time
import numpy as np
from cvzone.HandTrackingModule import HandDetector

def simplify_text_for_signs(text):
    mapping = {
        "are you going": "you go",
        "are you": "you",
        "do you know": "you know",
        "how are you": "how you",
        "i am fine": "i fine",
        "am i": "i",
        "can you": "you",
    }
    text = text.lower()
    for phrase, simplified in mapping.items():
        text = text.replace(phrase, simplified)
    return text

def render_ui(source_languages, SignPlayer, speech_to_text, translate_text, text_to_speech,
              play_sign_video, interpreter, input_d, output_d, labels):

    # CSS Styling with white and green theme
    st.markdown("""
        <style>
        /* General Styling */
        .stApp {
            background: #FFFFFF;
            color: #000000;
        }
        .block-container {
            padding: 2.5rem 2.5rem 0.25rem;
            background: #FFFFFF;
            border-radius: 12px;
            max-width: 1100px;
            margin: 0.5rem auto;
        }

        /* Navigation Bar */
        .navbar {
            background: #F0F5F1;
            padding: 0.8rem;
            border-radius: 8px;
            margin-bottom: 0.8rem;
            text-align: center; /* Center the content */
        }
        .navbar a {
            color: #176B45;
            font-size: 1rem;
            font-weight: 500;
            text-decoration: none;
            padding: 0.4rem 0.8rem;
            border-radius: 4px;
        }
        .navbar a:hover {
            background: #DDF1E4;
        }

        /* Sidebar Styling */
        .sidebar .sidebar-content {
            background: #F0F5F1;
            color: #202923;
            padding: 1.5rem;
            border-radius: 8px;
        }
        .sidebar .sidebar-content h2 {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: #176B45;
        }
        .sidebar .sidebar-content p, .sidebar .sidebar-content li {
            font-size: 0.9rem;
            line-height: 1.5;
            color: #FFFFFF;
        }
        .sidebar-link {
            display: block;
            font-size: 0.95rem;
            padding: 0.5rem 0;
            color: #FFFFFF;
        }
        .sidebar-link:hover {
            color: #176B45;
            font-weight: 500;
        }

        /* Sample Signs Section */
        .sample-signs-container {
            margin-top: 1.5rem;
        }
        .sample-sign-button {
            display: block;
            width: 100%;
            padding: 0.6rem;
            margin: 0.4rem 0;
            background: #E0E0E0;
            color: #000000;
            border-radius: 6px;
            text-align: center;
            font-size: 0.9rem;
            font-weight: 400;
        }
        .sample-sign-button:hover {
            background: #DDF1E4;
            color: #000000;
        }

        /* Header Styling */
        .header-container {
            text-align: center;
            padding: 2rem 1rem;
            background: #F0F5F1;
            color: #202923;
            border-radius: 12px;
            margin-bottom: 1.5rem;
        }
        .header-container h1 {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.4rem;
            color: #176B45;
        }
        .header-container p {
            font-size: 1rem;
            color: #FFFFFF;
        }
        .header-container svg {
            margin-top: 1rem;
        }

        /* Tabs Styling */
        .stTabs [data-baseweb="tab-list"] {
            background: #FFFFFF;
            border-radius: 8px;
            padding: 0.4rem;
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 0.95rem;
            padding: 0.6rem 1.2rem;
            border-radius: 6px;
            color: #000000;
            background: #E0E0E0;
        }
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background: #176B45;
            color: #FFFFFF;
            font-weight: 500;
        }
        .stTabs [data-baseweb="tab"]:hover {
            background: #DDF1E4;
            color: #000000;
        }

        .st-key-nav_home button,
        .st-key-nav_speech button,
        .st-key-nav_sign button,
        .st-key-nav_detect button {
            width: 100%;
            height: 3.1rem;
            min-height: 3.1rem;
            box-sizing: border-box;
            font-size: 1rem;
            font-weight: 600;
        }

        .st-key-home_card_speech [data-testid="stImage"] img,
        .st-key-home_card_sign [data-testid="stImage"] img,
        .st-key-home_card_detect [data-testid="stImage"] img {
            width: 100%;
            height: 125px;
            object-fit: cover;
            border-radius: 4px;
        }

        .st-key-home_intro h1 {
            font-size: 2rem;
            margin-bottom: 0.25rem;
        }
        .st-key-home_intro h3 {
            font-size: 1.25rem;
            margin-top: 0;
            margin-bottom: 0.4rem;
        }
        .st-key-home_intro p {
            line-height: 1.4;
        }
        .st-key-home_intro h1,
        .st-key-home_intro h3,
        .st-key-home_intro p {
            text-align: center;
        }
        .st-key-home_intro p {
            max-width: 850px;
            margin-right: auto;
            margin-left: auto;
        }

        /* Input and Selectbox Styling */
        .stTextInput>div>input, .stTextArea textarea, .stSelectbox select {
            border-radius: 8px;
            border: 1px solid #D5E0D8;
            background: #FFFFFF;
            padding: 0.6rem;
            font-size: 0.9rem;
            color: #000000;
        }

        /* Slider Styling */
        .stSlider [data-baseweb="slider"] {
            background: none;
        }
        .stSlider [data-baseweb="slider"] div[role="slider"] {
            background: #176B45;
        }

        /* Responsive Adjustments */
        @media (max-width: 768px) {
            .block-container {
                padding: 1rem;
            }
            .header-container h1 {
                font-size: 1.8rem;
            }
            .header-container p {
                font-size: 0.9rem;
            }
            .stTabs [data-baseweb="tab"] {
                font-size: 0.85rem;
                padding: 0.5rem 0.8rem;
            }
            .sample-sign-button {
                font-size: 0.85rem;
                padding: 0.5rem;
            }
            .navbar a {
                font-size: 0.9rem;
                padding: 0.3rem 0.6rem;
            }
        }

        /* Ensure all text is black unless specified */
        h1, h2, h3, p, div, span, a, li, input, textarea, select {
            color: #000000;
        }
        </style>
    """, unsafe_allow_html=True)

    # ========================== SESSION STATE =========================== #
    if "player" not in st.session_state:
        st.session_state.player = SignPlayer()
    if "speech_input_text" not in st.session_state:
        st.session_state.speech_input_text = ""
    if "translated_text" not in st.session_state:
        st.session_state.translated_text = ""
    if "translated_output" not in st.session_state:
        st.session_state.translated_output = ""
    if "audio_ready" not in st.session_state:
        st.session_state.audio_ready = False
    if "current_words" not in st.session_state:
        st.session_state.current_words = []
    if "webcam_active" not in st.session_state:
        st.session_state.webcam_active = False
    if "sign_input_text" not in st.session_state:
        st.session_state.sign_input_text = st.session_state.translated_text
    def render_home():
        with st.container(horizontal_alignment="center", key="home_intro"):
            st.title("SignEase")
            st.subheader("Make every conversation easier to follow.")
            st.write(
                "Speak or type in Tamil, Sinhala, Chinese, or English, then see and hear "
                "the English translation. Explore matching sign clips or show a hand sign "
                "to the camera to see what the model recognizes."
            )
        st.space(4)
        st.subheader("Choose where to start")

        cards = [
            (
                "Speech translator",
                "Record or type a phrase in one of four languages, then read and listen to its English translation.",
                "https://images.pexels.com/photos/8512149/pexels-photo-8512149.jpeg?auto=compress&w=1260&h=750&dpr=1",
                "Photo by Artem Podrez / Pexels",
                "https://www.pexels.com/photo/woman-sitting-on-a-wooden-chair-with-earpods-waving-on-a-video-call-8512149/",
                speech_page,
                "navcard_speech",
                ":material/mic:",
            ),
            (
                "Text to sign",
                "Type a word or phrase and watch the matching sign-language clips from the project library.",
                "https://thumb.wikimedia.org/wikipedia/commons/thumb/6/64/Sign_language_communicator.jpg/960px-Sign_language_communicator.jpg",
                "Photo by Myblueberet / Wikimedia Commons · CC BY-SA 4.0",
                "https://commons.wikimedia.org/wiki/File:Sign_language_communicator.jpg",
                sign_page,
                "navcard_sign",
                ":material/sign_language:",
            ),
            (
                "Sign detector",
                "Show a hand pose to your camera and get a prediction from the model’s supported sign labels.",
                "https://thumb.wikimedia.org/wikipedia/commons/thumb/6/65/Signer_James_Rowe_2014-12-07_DSCF0926_crop.jpg/960px-Signer_James_Rowe_2014-12-07_DSCF0926_crop.jpg",
                "Photo by Mary Mark Ockerbloom / Wikimedia Commons · CC0",
                "https://commons.wikimedia.org/wiki/File:Signer_James_Rowe_2014-12-07_DSCF0926_crop.jpg",
                detect_page,
                "navcard_detect",
                ":material/videocam:",
            ),
        ]

        columns = st.columns(3, gap="medium", vertical_alignment="top")
        for column, card in zip(columns, cards):
            title, description, image_url, credit, credit_url, target_page, key, icon = card
            card_key = key.replace("navcard_", "home_card_")
            with column:
                with st.container(border=True, height="stretch", key=card_key):
                    st.image(image_url, width="stretch")
                    st.subheader(title)
                    st.write(description)
                    st.markdown(f"[Photo credit]({credit_url}) · {credit}")
                    if st.button(
                        f"Open {title.lower()}",
                        key=key,
                        icon=icon,
                        type="primary",
                        width="stretch",
                    ):
                        st.switch_page(target_page)

    def render_speech_page():
        st.title("Speech translator")
        st.write(
            "Record or type a message in Tamil, Sinhala, Chinese, or English. "
            "The app translates it into English and reads the result aloud."
        )
        from_language = st.selectbox(
            "Source language", source_languages, index=3, key="speech_source_language"
        )
        speech_input = st.text_area(
            "Your text", value=st.session_state.speech_input_text, height=130
        )
        st.session_state.speech_input_text = speech_input

        record_col, translate_col, clear_col = st.columns(3)
        with record_col:
            if st.button("Record", icon=":material/mic:", width="stretch"):
                st.session_state.speech_input_text = speech_to_text(from_language)
                st.rerun()

        with translate_col:
            if st.button("Translate", icon=":material/language:", type="primary", width="stretch"):
                if st.session_state.speech_input_text.strip():
                    translated = translate_text(
                        st.session_state.speech_input_text, from_language
                    )
                    st.session_state.translated_text = translated
                    st.session_state.translated_output = translated
                    st.session_state.sign_input_text = translated
                    st.session_state.audio_ready = True
                    st.rerun()
                else:
                    st.warning("Enter text or record a phrase first.")

        with clear_col:
            if st.button("Clear", icon=":material/delete:", width="stretch"):
                st.session_state.speech_input_text = ""
                st.session_state.translated_text = ""
                st.session_state.translated_output = ""
                st.session_state.sign_input_text = ""
                st.session_state.audio_ready = False
                st.rerun()

        st.text_area(
            "English translation", key="translated_output", height=130
        )
        if st.session_state.audio_ready:
            text_to_speech(st.session_state.translated_text)
            st.session_state.audio_ready = False

    def render_sign_page():
        st.title("Text to sign")
        st.write(
            "Enter a word or phrase to play its matching sign clips. Available "
            "clips play in sequence; phrases without a matching clip use word-by-word playback."
        )
        st.text_input("Text to sign", key="sign_input_text")
        playback_speed = st.slider("Playback speed", 0.25, 2.0, 1.0, 0.25)

        if st.button("Play signs", icon=":material/play_arrow:", type="primary"):
            if st.session_state.sign_input_text.strip():
                simplified_text = simplify_text_for_signs(
                    st.session_state.sign_input_text
                )
                st.session_state.current_words = simplified_text.split()
                video_paths = st.session_state.player.process_input(simplified_text)
                play_sign_video(video_paths, playback_speed)
            else:
                st.warning("Enter text to play its sign clips.")

    def render_detect_page():
        st.title("Sign detector")
        st.write(
            "Show a hand pose to your webcam. The detector identifies signs from the "
            "classes included with the model."
        )
        if st.button("Toggle webcam", icon=":material/videocam:"):
            st.session_state.webcam_active = not st.session_state.webcam_active
            st.rerun()

        if st.session_state.webcam_active:
            if interpreter is None:
                st.error("Cannot start detection: model not loaded.")
                st.session_state.webcam_active = False
            else:
                try:
                    cap = cv2.VideoCapture(0)
                    if not cap.isOpened():
                        st.error("Failed to access webcam.")
                        st.session_state.webcam_active = False
                    else:
                        detector = HandDetector(maxHands=2)
                        frame_placeholder = st.empty()

                        while st.session_state.webcam_active:
                            ret, frame = cap.read()
                            if not ret:
                                st.error("Failed to capture video frame.")
                                break

                            output_frame = frame.copy()
                            hands, _ = detector.findHands(frame)
                            for hand in hands:
                                hand_type = hand["type"].lower()
                                x, y, width, height = hand["bbox"]
                                crop = frame[
                                    max(0, y - 20):y + height + 20,
                                    max(0, x - 20):x + width + 20,
                                ]
                                if crop.size == 0:
                                    continue

                                resized = cv2.resize(crop, (224, 224))
                                data = np.expand_dims(resized.astype(np.float32) / 255.0, 0)
                                interpreter.set_tensor(input_d[0]["index"], data)
                                interpreter.invoke()
                                prediction = interpreter.get_tensor(output_d[0]["index"])[0]
                                label_index = int(np.argmax(prediction))
                                confidence = float(prediction[label_index])
                                label = labels[label_index] if label_index < len(labels) else "Unlabeled sign"
                                text = f"{label.title()} ({confidence:.2f})"
                                cv2.putText(
                                    output_frame,
                                    text,
                                    (max(5, x), max(25, y - 12)),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.7,
                                    (24, 90, 55),
                                    2,
                                )
                                color = (255, 128, 0) if hand_type == "left" else (0, 128, 255)
                                cv2.rectangle(
                                    output_frame,
                                    (max(0, x - 20), max(0, y - 20)),
                                    (x + width + 20, y + height + 20),
                                    color,
                                    2,
                                )

                            frame_placeholder.image(
                                cv2.cvtColor(output_frame, cv2.COLOR_BGR2RGB),
                                width="stretch",
                            )
                            time.sleep(0.03)
                        cap.release()
                except Exception as error:
                    st.error(f"Webcam error: {error}")
                    st.session_state.webcam_active = False

    home_page = st.Page(
        render_home, title="Home", url_path="home", icon=":material/home:"
    )
    speech_page = st.Page(
        render_speech_page,
        title="Speech translator",
        url_path="speech-translator",
        icon=":material/mic:",
    )
    sign_page = st.Page(
        render_sign_page,
        title="Text to sign",
        url_path="text-to-sign",
        icon=":material/sign_language:",
    )
    detect_page = st.Page(
        render_detect_page,
        title="Sign detector",
        url_path="sign-detector",
        icon=":material/videocam:",
    )
    page = st.navigation(
        [home_page, speech_page, sign_page, detect_page], position="hidden"
    )

    nav_items = [
        ("home", home_page),
        ("speech", speech_page),
        ("sign", sign_page),
        ("detect", detect_page),
    ]
    nav_columns = st.columns([0.1, 2.4, 2.4, 2.4, 2.4, 0.1], gap="small")
    for column, (key, target_page) in zip(nav_columns[1:5], nav_items):
        with column:
            if st.button(
                target_page.title,
                key=f"nav_{key}",
                icon=target_page.icon,
                type="primary" if page.title == target_page.title else "secondary",
                width="stretch",
                wrap=True,
            ):
                st.switch_page(target_page)

    st.space("small" if page.title == "Home" else "medium")
    page.run()