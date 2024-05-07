import sys

import pyttsx3
import sounddevice as sd
import soundfile as sf
import whisper
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QTextEdit, QWidget

from llm_integration import query_gpt
import speech_recognition as sr


class SpeechWorker(QThread):
    finished = pyqtSignal(str)

    def __init__(self, model, tts_engine):
        super().__init__()
        self.model = model
        self.tts_engine = tts_engine

    def run(self):
        fs = 44100
        seconds = 5
        recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
        sd.wait()
        audio_path = "output.wav"
        sf.write(audio_path, recording, fs)

        result = self.model.transcribe(audio_path)
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
        # self.textEdit.append("Processing... Please wait")
        # self.worker = SpeechWorker(self.model, self.tts_engine)
        # self.worker.finished.connect(self.speak)
        # self.worker.start()
        listener = sr.Recognizer()
        print('Listening for a command')

        with sr.Microphone() as source:  # uses computer default mic
            listener.pause_threshold = 2
            input_speech = listener.listen(source)

        print("Understanding...")
        query = listener.recognize_google(input_speech, language='en_us')
        print(f'The input speech was: {query}')

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
