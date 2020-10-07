import os
import configparser


class ConfigException(Exception):
    pass


class ConfigReader:
    def __init__(self, config_file_path: str):
        """
        Read parameters from config file
        """
        # Initialize config parser class
        cfg = configparser.ConfigParser()
        self.cfg = cfg

        if not os.path.isfile(config_file_path):
            raise ConfigException(f"Config file does not exist in given file path: {config_file_path}")

        # Read module specific config reader
        cfg.read(config_file_path)
        self.__init_audio(cfg)
        self.__init_model(cfg)

    def __init_audio(self, cfg: configparser.ConfigParser):
        """
        Extract parameters from audio field in config file
        :param cfg: Config Reader class
        """
        try:
            self.channel = int(cfg.get("audio", "channel"))
            self.frame_second = float(cfg.get("audio", "frame_second"))
            self.sample_rate = int(cfg.get("audio", "sample_rate"))
            self.db_threshold = int(cfg.get("audio", "db_threshold"))
            self.fft_size = int(cfg.get("audio", "fft_size"))
            self.num_mels = int(cfg.get("audio", "num_mels"))
            self.feature = str(cfg.get("audio", "feature"))
        except Exception as err:
            raise ConfigException(f"Error while reading parameter for audio: {err}")

    def __init_model(self, cfg: configparser.ConfigParser):
        """
        Extract parameters from model field in config file
        :param cfg: Config Reader class
        """
        try:
            self.model_file_path = str(cfg.get("model", "model_file_path"))
            self.labels_file_path = str(cfg.get("model", "labels_file_path"))
            self.prediction_threshold = float(cfg.get("model", "prediction_threshold"))
        except Exception as err:
            raise ConfigException(f"Error while reading parameter for model: {err}")
