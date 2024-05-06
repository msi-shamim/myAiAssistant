import sys
import platform

import pyttsx3
import soundfile as sf
import whisper
import sounddevice as sd
import speech_recognition as sr
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QTextEdit, QWidget

from llm_integration import query_gpt


class SpeechWorker(QThread):
    finished = pyqtSignal(str)

    def __init__(self, model, tts_engine):
        super().__init__()
        self.model = model
        self.tts_engine = tts_engine

    def run(self):
        if platform.system() == "Windows":
            # Use speech_recognition for Windows
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Speak Now...")
                audio = r.listen(source)

            try:
                # Convert recorded speech to text
                text = r.recognize_google(audio)
                print("You said: " + text)
            except sr.UnknownValueError:
                text = "Could not understand audio"
                print("Could not understand audio")
            except sr.RequestError as e:
                text = "Could not request results from Google Speech Recognition service; {0}".format(e)
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
        else:
            # Use sounddevice for macOS and other platforms
            fs = 44100
            seconds = 5
            recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
            sd.wait()
            audio_path = "output.wav"
            sf.write(audio_path, recording, fs)

            text = self.model.transcribe(audio_path)

        # Process text using whisper and GPT
        result = self.model.transcribe(text)
        gpt_reply = query_gpt(result["text"])
        self.finished.emit(gpt_reply)


class MainWindow(QMainWindow):
    def __init__(self, model, tts_engine):
        super().__init__()
        self.model = model
        self.setGeometry(100, 100, 300, 400)
        self.setWindowTitle("My AI Assistant")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.textEdit = QTextEdit()
        self.textEdit.setPlaceholderText("Speak into the microphone and your speech will appear here...")

        self.listen_button = QPushButton()
        self.listen_button.setIcon(QIcon('microphone.png'))  # Mic icon button
        self.listen_button.setFixedSize(48, 48)
        self.listen_button.clicked.connect(self.listen)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.textEdit)
        self.layout.addWidget(self.listen_button, alignment=Qt.AlignRight)  # Button at the bottom right

        self.tts_engine = tts_engine

    def listen(self):
        self.textEdit.append("Processing... Please wait")
        self.worker = SpeechWorker(self.model, self.tts_engine)
        self.worker.finished.connect(self.speak)
        self.worker.start()

    def speak(self, text):
        self.textEdit.append(text)
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()


def main():
    app = QApplication(sys.argv)
    tts_engine = pyttsx3.init()
    tts_engine.setProperty('rate', 185)
    model = whisper.load_model("small")  # Load the model once and pass it to MainWindow
    window = MainWindow(model, tts_engine)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
