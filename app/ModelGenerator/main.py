import os
import numpy as np
import pandas as pd

from app.ModelGenerator.Training_Models import CNNModel
import PIL
import scipy


def ModelGenerator(ModelPath, classesDirs, ModelName, epochs: int = 60, batchSize: int = 50):
    # Example usage:
    input_shape = (256, 256, 3)  # Input image shape (height, width, channels)

    num_classes = len(classesDirs)
    model = CNNModel(input_shape, num_classes, ModelName)
    model.compile_model()

    classesDirs = pd.DataFrame(
        {'path': classesDirs, 'label': [os.path.basename(path) for path in classesDirs]})
    print(classesDirs.head()['label'])
    model.train_model(classesDirs, batchSize, epochs)

    model_path = ModelPath  # Path to save the trained model
    model.save_model(model_path)
