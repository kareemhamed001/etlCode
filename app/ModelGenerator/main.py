import os
import numpy as np
from app.ModelGenerator.Training_Models import CNNModel
import PIL
import scipy


def ModelGenerator(ModelPath,traindir,ModelName,epochs:int=60,batchSize:int=50):
    # Example usage:
    input_shape = (256, 256, 3)  # Input image shape (height, width, channels)
    train_dir = traindir
    num_classes = sum([1 for item in os.listdir(train_dir) if os.path.isdir(
        os.path.join(train_dir, item))])  # used to count number of dirs i trianing dir (number of class)
    model = CNNModel(input_shape, num_classes, ModelName)
    model.compile_model()


    model.train_model(train_dir, batchSize, epochs)

    model_path = ModelPath  # Path to save the trained model
    model.save_model(model_path)