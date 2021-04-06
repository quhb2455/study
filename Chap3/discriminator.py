import sys
import numpy as np

from keras.layers import  Input, Dense, Reshape, Flatten, Dropout
from keras.layers.advanced_activations import LeakyReLU
from keras.models import Sequential, Model
from keras.optimizers import Adam
from keras.utils import plot_model


class Discriminator(object) :
    def __init__(self, width=28, height=28, channels=1, latent_size=100):
        self.CAPACITY = width * height * channels
        self.SHAPE = (width, height, channels)
        self.OPTIMIZER = Adam(lr=0.0002, decay=8e-9)

        # model initialize
        self.Discriminator = self.model()

        # model compile
        self.Discriminator.complie(loss='binary_crossentropy', optimizer=self.OPTIMIZER, metrics=['accuracy'])

        # summary
        self.Discriminator.summary()

    # model define
    def model(self):
        model = Sequential()
        model.add(Flatten(input_shape=self.SHAPE))
        model.add(Dense(self.CAPACITY, input_shape=self.SHAPE))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dense(int(self.CAPACITY / 2)))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dense(1, activation='sigmoid'))
        return model

    def summary(self):
        return self.Discriminator.summary()

    def save_model(self):
        plot_model(self.Discriminator.model,
                   to_file='./model/discriminator.png')