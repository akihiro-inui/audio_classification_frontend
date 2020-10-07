import os
import sys
sys.path.insert(0, os.getcwd())
import pyaudio
import numpy as np
import time
from src.backend.predict.model import load_model
from src.backend.utils.audio import select_mic
from src.backend.utils.config_reader import ConfigReader
from src.backend.utils.file import read_json_file
from src.backend.feature.feature_selector import FeatureSelector


class StreamerException(Exception):
    pass

cfg = ConfigReader("config.ini")
model = load_model(cfg.model_file_path)
FS = FeatureSelector("config.ini")
extractor = FS.select_feature(cfg.feature)

# Select microphone
device_index = select_mic()
labels = read_json_file(cfg.labels_file_path)


def predictor(input_data, frame_count, time_info, status_flags):
    """
    Call back function for audio streamer
    1. Read audio data from buffer
    2. Extract feature
    3. Make model prediction
    :param input_data: Input audio data from buffer
    :param frame_count: Frame count
    :param time_info: Streamer Time
    :param status_flags: Streamer status
    :return: input_data: Return data
    :retrun: pyaudio.paContinue: Return this to continue streaming
    """
    # Convert audio buffer to numpy array
    audio_signal = np.frombuffer(input_data, dtype=np.int16) / 32768.0
    audio_signal / max(abs(audio_signal[:]))
    feature = extractor(audio_signal)

    # Reshape input audio array for model input
    feature = feature.reshape(-1, feature.shape[0], feature.shape[1], 1)

    # Make model prediction
    prediction = model.predict(feature)
    predicted_label_index = np.argmax(prediction[0])
    print(f"Predicted class: {labels[str(predicted_label_index)]} ({prediction[0, predicted_label_index]})")
    return (input_data, pyaudio.paContinue)

while(1):
    # Build audio streamer
    p = pyaudio.PyAudio()
    streamer = p.open(format=pyaudio.paInt16,
                      channels=cfg.channel,
                      rate=cfg.sample_rate,
                      input=True,
                      stream_callback=predictor,
                      frames_per_buffer=int(cfg.frame_second * cfg.sample_rate),
                      input_device_index=device_index)

    ##############################
    # Start Non-Blocking Stream
    ##############################
    streamer.start_stream()
    while streamer.is_active():
        time.sleep(0.1)
