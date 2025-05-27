import streamlit as st
import io
from utils import audio_to_text, english_to_german, text_to_audio, get_similarity_and_feedback
import os
from streamlit_mic_recorder import mic_recorder

PRESET_PHRASES = [
    ("Wie geht es Ihnen?", "How are you?"),
    ("Können Sie mir bitte helfen?", "Can you please help me?"),
    ("Wo haben Sie Schmerzen?", "Where do you have pain?"),
    ("Ich werde Ihren Blutdruck messen.", "I will measure your blood pressure."),
    ("Bitte nehmen Sie Ihre Medikamente.", "Please take your medication.")
]

def initialize_session_state():
    defaults = {
        "tts_ready": False,
        "german_text": "",
        "generated_audio": None,
        "attempts": [],
        "selected_phrase": PRESET_PHRASES[0]
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def display_header():
    st.set_page_config(page_title="German Pronunciation Practice", layout="centered")
    st.title("German Pronunciation Practice for Nurses")
    st.markdown("Practice German medical phrases and get feedback on your pronunciation.")

def display_phrase_and_audio_section():
    with st.container():
        st.header("Step 1: Choose and Listen to a Phrase")
        st.markdown("Select a preset phrase or enter an English phrase to translate, then listen to it.")

        input_method = st.radio("Choose input method:", ["Select Preset Phrase", "Enter Custom Phrase"], horizontal=True)

        if input_method == "Select Preset Phrase":
            display_list = [f"{ger} - {eng}" for ger, eng in PRESET_PHRASES]
            try:
                current_phrase = f"{st.session_state.selected_phrase[0]} - {st.session_state.selected_phrase[1]}"
                default_index = display_list.index(current_phrase)
            except ValueError:
                default_index = 0
                st.session_state.selected_phrase = PRESET_PHRASES[0]

            selected_str = st.selectbox("Choose a phrase to practice:", display_list, index=default_index, key="phrase_select")
            selected_index = display_list.index(selected_str)
            st.session_state.selected_phrase = PRESET_PHRASES[selected_index]
            st.session_state.german_text = PRESET_PHRASES[selected_index][0]

        else:
            english_text = st.text_input(
                "Enter an English phrase to translate:",
                placeholder="For example: How are you feeling?",
                key="english_input"
            )
            if english_text:
                translated = english_to_german(english_text)
                st.session_state.german_text = translated
                st.session_state.selected_phrase = ("", "")  # Avoid indexing error in preset list

        # ✅ Always show the button but disable if no German text
        generate_disabled = not bool(st.session_state.german_text)
        if st.button("Generate and Play Audio", use_container_width=True, disabled=generate_disabled, key="generate_audio"):
            st.session_state.tts_ready = True
            st.session_state.generated_audio = text_to_audio(st.session_state.german_text)

        if st.session_state.tts_ready:
            st.markdown(f"**German Phrase:** {st.session_state.german_text}")
            if st.session_state.generated_audio:
                st.audio(st.session_state.generated_audio, format="audio/mp3")

def display_recording_section():
    with st.container():
        st.header("Step 2: Record Your Pronunciation")
        if not st.session_state.tts_ready:
            st.info("Please generate audio in Step 1 before recording.")
            st.button("Start Recording", disabled=True, use_container_width=True)
            return

        st.markdown("Record yourself saying the phrase and get feedback.")
        recorded_audio = mic_recorder(
            start_prompt="Start Recording",
            stop_prompt="Stop Recording",
            use_container_width=True,
            format="wav",
            key="recording"
        )

        if not recorded_audio:
            return

        st.audio(recorded_audio['bytes'], format="audio/wav")
        user_speech_text = audio_to_text(recorded_audio)
        feedback = get_similarity_and_feedback(st.session_state.german_text, user_speech_text)

        score = None
        if "Not applicable" not in feedback:
            score = float(feedback.split("%")[0].split(":")[1].strip())

        st.session_state.attempts.append({
            "text": user_speech_text,
            "feedback": feedback,
            "score": score if score is not None else 0
        })

        st.markdown(f"**Your Pronunciation:** {user_speech_text}")
        st.markdown(f"**Feedback:** {feedback}")

        display_progress()

def display_progress():
    if not st.session_state.attempts:
        return

    with st.container():
        st.header("Step 3: See Your Progress")
        st.markdown("Track how your pronunciation improves with each try.")
        scores = [attempt["score"] for attempt in st.session_state.attempts]
        st.line_chart(scores)
        st.markdown(f"**Total Attempts:** {len(st.session_state.attempts)}")
        for i, attempt in enumerate(st.session_state.attempts, 1):
            st.markdown(f"**Attempt {i}:** {attempt['text']} - Score: {attempt['score']}%")

def main():
    initialize_session_state()
    display_header()
    display_phrase_and_audio_section()
    display_recording_section()

if __name__ == "__main__":
    main()
