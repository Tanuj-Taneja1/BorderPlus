# German Pronunciation Practice for Nurses
This is a **Streamlit-based web application** developed as part of a Border Plus assignment to help nurses practice German pronunciation. Users can listen to preset or custom-translated German phrases, record their pronunciation, and receive **real-time AI feedback**.

**Live App**: [https://borderplus-1.streamlit.app/](https://borderplus-1.streamlit.app/)

---

## ⭐ Features

- Choose from **preset German phrases** or input your own in English.
- Translate custom phrases to **German using the Gemini API**.
- Generate **German audio using gTTS**.
- Record your voice and get feedback on **pronunciation similarity**.
- Receive **AI-generated improvement suggestions**.
- Visualize your **pronunciation progress over time**.

---

## 🛠️ Technologies Used

- **Streamlit** – for building the interactive web app
- **Google Gemini API** – for translation and transcription
- **gTTS (Google Text-to-Speech)** – for German speech synthesis
- **Resampy, Soundfile, NumPy** – for audio processing
- **streamlit-mic-recorder** – for voice recording in-browser

---

## 📁 File Structure

```
├── app.py              # Main Streamlit app
├── utils.py            # Helper functions (translation, feedback, audio)
├── requirements.txt    # Python dependencies
```

---

## 🚀 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/Tanuj-Taneja1/BorderPlus.git
   cd BorderPlus
   ```

2. **Install dependencies**
   (Recommended: Use a virtual environment)
   ```bash
   pip install -r requirements.txt
   ```

3. **Add Gemini API Key**

   - Option 1: Create a `.env` file
     ```
     GEMINI_API_KEY=your_google_genai_key_here
     ```

   - Option 2: Use Streamlit secrets
     Create `.streamlit/secrets.toml`:
     ```toml
     [general]
     GEMINI_API_KEY = "your_google_genai_key_here"
     ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

---

