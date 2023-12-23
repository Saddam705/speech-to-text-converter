from flask import Flask, render_template, request
import speech_recognition as sr
from pydub import AudioSegment
import tempfile

app = Flask(__name__)

def convert_audio_to_text(audio_data):
    recognizer = sr.Recognizer()

    try:
        text = recognizer.recognize_google(audio_data)  # You can replace this with other API calls
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Error making the request: {e}"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded_file = request.files["file"]
        if uploaded_file:
            recognizer = sr.Recognizer()  # Define the recognizer here
            audio_data = AudioSegment.from_file(uploaded_file, format=uploaded_file.filename.split('.')[-1])

            # Create a temporary WAV file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
                audio_data.export(temp_wav.name, format="wav")
                temp_wav.seek(0)

                # Use SpeechRecognition with the temporary WAV file
                with sr.AudioFile(temp_wav.name) as temp_audio:
                    result = convert_audio_to_text(recognizer.record(temp_audio))

            return render_template("index.html", result=result)
    
    return render_template("index.html", result=None)

if __name__ == "__main__":
    app.run(debug=True)