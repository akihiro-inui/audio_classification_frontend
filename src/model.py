import os
import tensorflow as tf


def load_model(model_file_path: str):
    """
    Load trained model file
    :param model_file_path: Model file path
    :return: Trained model
    """
    # Assert if model file does not exist in the given file path
    assert os.path.exists(model_file_path), "Model file does not exist"

    return tf.keras.models.load_model(model_file_path)
