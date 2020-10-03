import os
import sys
sys.path.insert(0, os.getcwd())
import time
import pyaudio
import numpy as np
from src.model import load_model
from src.audio import select_mic
from src.utils.config_reader import ConfigReader
from src.utils.file import read_json_file
from src.feature.feature_selector import FeatureSelector


class StreamerException(Exception):
    pass


class AudioStreamer:
    def __init__(self, config_file_path: str):
        """
        param config_file_path: Config file path
        """
        # Read parameters from config file
        self.cfg = ConfigReader(config_file_path)
        self.model = load_model(self.cfg.model_file_path)
        self.FS = FeatureSelector(config_file_path)
        self.extractor = self.FS.select_feature(self.cfg.feature)
        self.labels = read_json_file(self.cfg.labels_file_path)

    def build_streamer(self):
        """
        Read parameter from config file, build audio streamer with selected device index.
        :return: Pyaudio streamer
        """
        try:
            # Select microphone
            device_index = select_mic()

            # Build audio streamer
            p = pyaudio.PyAudio()
            streamer = p.open(format=pyaudio.paInt16,
                              channels=self.cfg.channel,
                              rate=self.cfg.sample_rate,
                              input=True,
                              stream_callback=self.predictor,
                              frames_per_buffer=int(self.cfg.frame_second*self.cfg.sample_rate),
                              input_device_index=device_index)
            return streamer
        except Exception as err:
            raise StreamerException(f"Error while building streamer {err}")

    def run_streamer(self, streamer):
        """
        Run audio streamer and make prediction on audio chunk
        :param streamer: Pyaudio Streamer class
        """
        # Run audio streamer
        while True:
            streamer.start_stream()

    def stop_streamer(self, streamer):
        """
        Stop audio streamer and make prediction on audio chunk
        :param streamer: Pyaudio Streamer class
        """
        # Run audio streamer
        stop_streamer.stop_stream()

    def predictor(self, input_data, frame_count, time_info, status_flags):
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
        feature = self.extractor(audio_signal)

        # Reshape input audio array for model input
        feature = feature.reshape(-1, feature.shape[0], feature.shape[1], 1)

        # Make model prediction
        prediction = self.model.predict(feature)
        predicted_label_index = np.argmax(prediction[0])
        print(f"Predicted class: {self.labels[str(predicted_label_index)]} ({prediction[0, predicted_label_index]})")
        return (input_data, pyaudio.paContinue)


if __name__ == "__main__":
    AUS = AudioStreamer('config.ini')
    streamer = AUS.build_streamer()
    AUS.run_streamer(streamer)
