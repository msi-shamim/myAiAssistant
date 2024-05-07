import sys
import time

import pyttsx3
import sounddevice as sd
import soundfile as sf
import whisper
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QRunnable, QThreadPool
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QTextEdit, QWidget
from playsound import playsound
from gtts import gTTS
import asyncio
from llm_integration import query_gpt
import threading

class SpeechWorker(QThread):
    finished = pyqtSignal(str)

    def __init__(self, model):
        super().__init__()
        self.model = model

    def run(self):
        fs = 44100
        seconds = 5
        recording = sd.rec(int(seconds * fs), samplerate=44100, channels=1)
        sd.wait()
        audio_path = "output.wav"
        sf.write(audio_path, recording, fs)
        result = self.model.transcribe(audio_path)
        gpt_reply = query_gpt(result["text"])

        # gpt_reply = result["text"]
        self.finished.emit(gpt_reply)


class PlayWorker(QThread):
    finished = pyqtSignal(str)
    def __init__(self, text):
        super().__init__()
        self.text = text

    def run(self):
        tts = gTTS(self.text)
        tts.save('audio/temp.mp3')
        playsound('audio/temp.mp3')
        # self.finished.emit(gpt_reply)


class MainWindow(QMainWindow):
    def __init__(self, model):
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

    def listen(self):
        self.textEdit.append("Processing... Please wait")
        self.worker = SpeechWorker(self.model)
        self.worker.finished.connect(self.speak)
        self.worker.start()

    def play_audio(self, text):
        time.sleep(1)
        tts = gTTS(text)
        tts.save('audio/temp.mp3')
        playsound('audio/temp.mp3')
        
    def print_text(self, text):
        time.sleep(1)
        self.textEdit.append(text)


    def speak(self, text):
        self.textEdit.append(text)
        self.worker1 = PlayWorker(text)
        # self.worker.finished.connect(self.speak)
        self.worker1.start()

        # thread1 = threading.Thread(target=self.play_audio, args=(text,))
        # # thread2 = threading.Thread(target=self.print_text, args=(text,))
        # thread1.start()
        # # thread2.start()
        # thread1.join()
        # thread2.join()

        # asyncio.run(self.play_audio(text))
        # asyncio.gather(
        #     self.print_text(text),
        #     self.play_audio(text)
        # )



def main():
    app = QApplication(sys.argv)
    # tts_engine = pyttsx3.init()
    # tts_engine.setProperty('rate', 185)
    model = whisper.load_model("small")  # Load the model once and pass it to MainWindow
    window = MainWindow(model)
    window.show()
    app.exec_()
    # sys.exit(app.exec_())


if __name__ == "__main__":
    main()
