import os
from google import genai
from google.genai import types
import soundfile as sf
import io
from gtts import gTTS
import resampy
import numpy as np
from dotenv import load_dotenv
import streamlit as st

try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

chat_session = None

def start_chat_session():
    global chat_session
    if chat_session is None:
        client = genai.Client(api_key=api_key)
        chat_session = client.chats.create(model="gemini-2.0-flash")
    return chat_session

def audio_to_text(audio_file):
    audio_bytes = audio_file['bytes']
    audio_buffer = io.BytesIO(audio_bytes)
    waveform, sample_rate = sf.read(audio_buffer)

    if sample_rate != 16000:
        waveform = resampy.resample(waveform, sample_rate, 16000)

    audio_buffer_resampled = io.BytesIO()
    sf.write(audio_buffer_resampled, waveform, 16000, format='WAV')
    audio_bytes_resampled = audio_buffer_resampled.getvalue()

    text_part = types.Part.from_text(text="Extract German speech from audio and output just the text")
    audio_part = types.Part.from_bytes(data=audio_bytes_resampled, mime_type="audio/wav")
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=[text_part, audio_part]
    )

    return response.text

def english_to_german(text):
    client = genai.Client(api_key=api_key)
    prompt =f"""Convert English Sentence below to German, Output just the final German text
                Sentence: {text}
                """
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt)
    return response.text

def text_to_audio(german_text):
    tts = gTTS(german_text, lang='de')
    mp3_io = io.BytesIO()
    tts.write_to_fp(mp3_io)
    mp3_io.seek(0)
    return mp3_io

def get_similarity_and_feedback(expected, spoken, output_language="English", spoken_language="German"):
    global chat_session
    chat_session = start_chat_session()
    
    if not spoken.strip():
        response_text = """Similarity: 0%
        Suggestion: It seems you didn't say anything. Please try recording your pronunciation again, speaking clearly into the microphone."""
        return response_text
    
    prompt = f"""
            You have to act as German language coach for Nurses learning German 
            Compare the expected sentence and the spoken sentence below.Try to be kind and helpfull and not too harsh in judgement 

            Expected: {expected}
            Spoken: {spoken}

            Your task:
            1. Identify any mispronounced or missing words.
            2. Suggest few lines of improvements kindly and clearly in points.
            3. Give an overall pronunciation similarity score from 0% to 100%.

            Respond entirely in {output_language} judging {spoken_language} expected and spoken sentences with the output format:

            Similarity: XX%
            Suggestion: ...
            
            Maintain context from previous comparisons if any.
    """
    response = chat_session.send_message_stream(prompt)
    response_text=""
    for chunk in response:
        response_text+=chunk.text
    return response_text