from abc import ABC, abstractmethod


class BaseFeature(ABC):
    """
    Base class for audio feature extraction
    All abstractmethod needs to be common methods in feature extractors
    """
    def __init__(self):
        pass

    @abstractmethod
    def apply(self, audio_data):
        raise NotImplementedError
