# My AI Assistant

This project is a voice command AI assistant for PCs, similar to Siri. It uses Whisper for voice recognition and pyttsx3 for text-to-speech functionality.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7+ installed
- Homebrew installed (for macOS users)

## Dependencies

### Using Homebrew

This project requires the following system dependencies installed via Homebrew:

```bash
brew install portaudio
brew install ffmpeg
```
### Using pip

Python dependencies should be installed via pip:

```bash
pip install openai-whisper
pip install pyttsx3
pip install PyQt5
pip install sounddevice
pip install numpy
pip install soundfile
```

### Setup

Clone the repo and navigate into the project directory: 

```bash
git clone https://github.com/msi-shamim/myAiAssistant.git
```
Goto project folder: 

```bash
cd myAiAssistant
```

Create a Python virtual environment and activate it: 

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install the required Python packages: 

```bash
pip install -r requirements.txt
```

### Running the Application

To run the application, execute: 

```bash
python main.py
```

### Contributing 

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch `(git checkout -b feature/AmazingFeature)`
3. Commit your Changes `(git commit -m 'Add some AmazingFeature')`
4. Push to the Branch `(git push origin feature/AmazingFeature)`
5. Open a Pull Request

### License

Distributed under the MIT License. See **'LICENSE'** for more information.

### Contact

[Email](mailto:im.msishamim@gmail.com) | [Website](https://msishamim.com) 

## Thank You
