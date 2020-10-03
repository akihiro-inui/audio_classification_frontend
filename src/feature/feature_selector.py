from src.utils.config_reader import ConfigReader
from src.feature.mel_spectrogram import MelSpectrogram
from src.utils.custom_error_handler import FeatureExtractionException


class FeatureSelector:
    def __init__(self, config_file_path: str):
        """
        Feature extraction wrapper
        Add new feature extraction method to "feature_type_map"
        :param config_file_path: Config file path
        """
        self.cfg = ConfigReader(config_file_path)
        self.mel_spectrogram = MelSpectrogram()
        # Feature extraction selector
        self.feature_type_map = {
            "mel_spectrogram": self.mel_spectrogram.apply
        }

    def select_feature(self, feature_name: str):
        """
        Select audio feature extractor from pre-defined function map
        :param feature_name: Name of feature
        """
        try:
            return self.feature_type_map[feature_name]
        except KeyError:
            raise FeatureExtractionException(f"Selected audio feature extractor '{feature_name}' does not exist")
        except Exception as err:
            raise FeatureExtractionException(f"Error while selecting audio feature extractor: {err}")
