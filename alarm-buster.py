import sounddevice as sd
import numpy as np
import simpleaudio as sa
import time
import wave

threshold = 0.0001
duration = 1 # in seconds
sampling_rate = 44100
times = 5
amplitude_factor = 5.0  # Increase this factor to increase the amplitude

audio_to_play = "alarm.wav"

def increase_amplitude(audio_file, factor):
    with wave.open(audio_file, 'rb') as wf:
        params = wf.getparams()
        frames = wf.readframes(wf.getnframes())
        audio_data = np.frombuffer(frames, dtype=np.int16)
        audio_data = np.clip(audio_data * factor, -32768, 32767).astype(np.int16)
        return audio_data.tobytes(), params

def detect_sound_and_respond():
    print("Listening for sounds...")
    while True:
        audio_data = sd.rec(int(sampling_rate * duration), samplerate=sampling_rate, channels=1)
        sd.wait()
        volume_norm = np.linalg.norm(audio_data) / len(audio_data)
        print(f"Detected volume: {volume_norm:.5f}")
        if volume_norm >= threshold:
            print("Sound detected! Playing response...")
            audio_data, params = increase_amplitude(audio_to_play, amplitude_factor)
            wave_obj = sa.WaveObject(audio_data, params.nchannels, params.sampwidth, params.framerate)
            for i in range(times):
                print(f"Playing sound: {i+1}/{times}")
                play_obj = wave_obj.play()
                play_obj.wait_done()
                time.sleep(1)
            break

detect_sound_and_respond()