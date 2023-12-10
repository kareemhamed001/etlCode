import os
import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Rescaling
from keras.applications import ResNet50, MobileNet, VGG16 ,VGG19, ResNet101,ResNet152
from keras.applications.inception_v3 import InceptionV3
from keras.models import Model
import pandas as pd

class CNNModel:
    def __init__(self, input_shape, num_classes, model:str):
        self.input_shape = input_shape
        self.num_classes = num_classes
        if model.lower() == 'vgg16':
            self.model = self.VGG16Model()
        elif model.lower() == 'vgg19':
            self.model = self.VGG19Model()
        elif model.lower() == 'custom':
            self.model = self.build_model()
        elif model.lower() == 'resnet50':
            self.model = self.ResNet50()
        elif model.lower() == 'resnet101':
            self.model = self.ResNet101()
        elif model.lower() == 'resnet152':
            self.model = self.ResNet152()
        elif model.lower() == 'mobilenet':
            self.model = self.MobileNet()
        elif model.lower() == 'inceptionv3':
            self.model = self.inception()
        else:
            print("Invalid model name. Choose from Custom, vgg16,vgg19, ResNet50, ResNet101, ResNet152, MobileNet, or inceptionv3.")
            exit()

    def build_model(self):
        try:
            model = Sequential()
            model.add(Rescaling(1.0 / 255.0, input_shape=self.input_shape))
            model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=self.input_shape))
            model.add(MaxPooling2D(pool_size=(2, 2)))
            model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
            model.add(MaxPooling2D(pool_size=(2, 2)))
            model.add(Flatten())
            model.add(Dense(128, activation='relu'))
            model.add(Dense(self.num_classes, activation='softmax'))
            return model
        except Exception as ex:
            print(ex)
            return ex

    def VGG16Model(self):
        try:
            base_model = VGG16(weights='imagenet',
                               include_top=False, input_shape=self.input_shape)
            x = Flatten()(base_model.output)
            x = Dense(128, activation='relu')(x)
            output = Dense(self.num_classes, activation='softmax')(x)

            model = Model(inputs=base_model.input, outputs=output)

            # Freeze the layers of the pre-trained model
            for layer in base_model.layers:
                layer.trainable = False

            return model
        except Exception as ex:
            print(ex)
            return ex

    def VGG19Model(self):
        try:
            base_model = VGG19(weights='imagenet',
                               include_top=False, input_shape=self.input_shape)
            x = Flatten()(base_model.output)
            x = Dense(128, activation='relu')(x)
            output = Dense(self.num_classes, activation='softmax')(x)

            model = Model(inputs=base_model.input, outputs=output)

            # Freeze the layers of the pre-trained model
            for layer in base_model.layers:
                layer.trainable = False

            return model
        except Exception as ex:
            print(ex)
            return ex
    def ResNet50(self):
        try:
            base_model = ResNet50(weights='imagenet',
                                   include_top=False, input_shape=self.input_shape)
            x = Flatten()(base_model.output)
            x = Dense(128, activation='relu')(x)
            output = Dense(self.num_classes, activation='softmax')(x)

            model = Model(inputs=base_model.input, outputs=output)

                # Freeze the layers of the pre-trained model
            for layer in base_model.layers:
                layer.trainable = False

            return model
        except Exception as ex:
            print(ex)
            return ex

    def MobileNet(self):
        try:
            base_model = MobileNet(weights='imagenet',
                                   include_top=False, input_shape=self.input_shape)
            x = Flatten()(base_model.output)
            x = Dense(128, activation='relu')(x)
            output = Dense(self.num_classes, activation='softmax')(x)

            model = Model(inputs=base_model.input, outputs=output)

                # Freeze the layers of the pre-trained model
            for layer in base_model.layers:
                layer.trainable = False

            return model
        except Exception as ex:
            print(ex)
            return ex

    def ResNet101(self):
        try:
            base_model = ResNet101(weights='imagenet',
                                   include_top=False, input_shape=self.input_shape)
            x = Flatten()(base_model.output)
            x = Dense(128, activation='relu')(x)
            output = Dense(self.num_classes, activation='softmax')(x)

            model = Model(inputs=base_model.input, outputs=output)

                # Freeze the layers of the pre-trained model
            for layer in base_model.layers:
                layer.trainable = False

            return model
        except Exception as ex:
            print(ex)
            return ex


    def ResNet152(self):
        try:
            base_model = ResNet152(weights='imagenet',
                                   include_top=False, input_shape=self.input_shape)
            x = Flatten()(base_model.output)
            x = Dense(128, activation='relu')(x)
            output = Dense(self.num_classes, activation='softmax')(x)

            model = Model(inputs=base_model.input, outputs=output)

                # Freeze the layers of the pre-trained model
            for layer in base_model.layers:
                layer.trainable = False

            return model
        except Exception as ex:
            print(ex)
            return ex

    def inception(self):
        try:
            base_model = InceptionV3(weights='imagenet',
                                   include_top=False, input_shape=self.input_shape)
            x = Flatten()(base_model.output)
            x = Dense(128, activation='relu')(x)
            output = Dense(self.num_classes, activation='softmax')(x)

            model = Model(inputs=base_model.input, outputs=output)

                # Freeze the layers of the pre-trained model
            for layer in base_model.layers:
                layer.trainable = False

            return model
        except Exception as ex:
            print(ex)
            return ex

    def compile_model(self):
        try:
            self.model.compile(loss='categorical_crossentropy',
                               optimizer='adam',
                               metrics=['accuracy'])
        except Exception as ex:
            print(ex)
            return ex

    def train_model(self, train_dir, batch_size, epochs):
        try:
            train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1.0 / 255)
            train_generator = train_datagen.flow_from_directory(directory=train_dir,
                                                                target_size=self.input_shape[:2],
                                                                batch_size=batch_size,
                                                                class_mode='categorical',
                                                                shuffle=True)

            self.model.fit(train_generator,
                           steps_per_epoch=train_generator.samples // batch_size,
                           epochs=epochs
                           )
        except Exception as ex:
            print(ex)
            return ex

    def save_model(self, model_path):
        try:
            self.model.save(model_path)
        except Exception as ex:
            print(ex)
            return ex

    def load_model(self, model_path):
        try:
            self.model = tf.keras.models.load_model(model_path)
        except Exception as ex:
            print(ex)
            return ex

    def predict(self, image_path):
        try:
            image = tf.keras.preprocessing.image.load_img(image_path, target_size=self.input_shape[:2])
            image = tf.keras.preprocessing.image.img_to_array(image)
            image = np.expand_dims(image, axis=0)
            image = image / 255.0
            prediction = self.model.predict(image)
            class_index = np.argmax(prediction)
            return class_index
        except Exception as ex:
            print(ex)
            return ex
