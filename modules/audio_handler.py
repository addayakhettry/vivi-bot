import pyttsx3
import os
import uuid

def generate_speech(text, output_dir="static/audio"):
    try:
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{uuid.uuid4().hex}.mp3"
        filepath = os.path.join(output_dir, filename)

        engine = pyttsx3.init()
        engine.setProperty("rate", 160)
        engine.save_to_file(text, filepath)
        engine.runAndWait()

        print(f"[Audio generated] {filepath}")
        return f"/static/audio/{filename}"
    except Exception as e:
        print(f"[Audio generation error] {e}")
        return None
