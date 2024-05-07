# import librosa
import numpy as np
# from scipy.io.wavfile import write as write_wav
from pydub import AudioSegment, silence
from pydub.silence import split_on_silence


def chun():
    sound_file = AudioSegment.from_wav("output.wav")
    audio_chunks = split_on_silence(sound_file,
        # must be silent for at least half a second
        min_silence_len=100,

        # consider it silent if quieter than -16 dBFS
        silence_thresh=-40
    )
    print(silence.detect_silence(AudioSegment.silent(2000)),
          silence.detect_nonsilent(
              sound_file,
              min_silence_len=100,

              # consider it silent if quieter than -16 dBFS
              silence_thresh=-20
          )
          )
    # non_silent_ranges = pydub.silence.detect_nonsilent(segment, min_silence_len=1000, silence_thresh=thresh)

    print(audio_chunks)
    for i, chunk in enumerate(audio_chunks):

        out_file = "chunk{0}.wav".format(i)
        print("exporting", out_file)
        chunk.export(out_file, format="wav")

chun()



def segment_audio_on_silence(audio_path, out_dir, min_silence_duration=0.01, sample_rate=None):
    # Load audio
    waveform, sampling_rate = librosa.load(audio_path, sr=sample_rate)

    # Detect silence
    eps = waveform.max() * 0.01  # Adjust this value based on your audio
    silence_mask = (np.abs(waveform) < eps).astype(np.uint8)

    # Find silence runs
    runs = np.where(np.diff(silence_mask) == 1)[0]
    run_lengths = np.diff(runs)

    # Filter out short silences
    min_silence_duration *= sampling_rate
    valid_run_indices = np.where(run_lengths > min_silence_duration)[0]

    # Segment audio based on silence
    segments = []
    for i in valid_run_indices:
        start = runs[i]
        end = runs[i + 1]
        segment = waveform[start:end]
        segments.append(segment)

    # Save segments
    for i, segment in enumerate(segments):
        out_file = f"sdfsd.wav"
        write_wav(out_file, sampling_rate, segment)
        print(f"Saved segment {i} to {out_file}")


# Usage
# segment_audio_on_silence("path/to/your/audio.wav", "path/to/output/directory")
