import numpy as np

from keras.datasets import mnist

from keras.models import Sequential

import keras
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Dropout

# Retrieve mnist dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# make image with zero to blank image
x_train[y_train==0] = np.zeros((28,28), dtype=np.uint8)
x_test[y_test==0] = np.zeros((28,28), dtype=np.uint8)

# Mnist images are 28x28 images
img_row = 28
img_col = 28

# Preprocess image so keras can use it
x_train = x_train.reshape(x_train.shape[0], img_row, img_col, 1)
x_test = x_test.reshape(x_test.shape[0], img_row, img_col, 1)

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255


# Convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, 10)
y_test = keras.utils.to_categorical(y_test, 10)

classifier = Sequential()

# Convolution and Pooling 1
classifier.add(Convolution2D(32, kernel_size=(5,5), padding='same', activation='relu', input_shape=(img_row, img_col, 1)))

classifier.add(MaxPooling2D(pool_size=(2,2), strides=2))

# Convolution and Pooling 2
classifier.add(Convolution2D(64, kernel_size=(5,5), padding='same', activation='relu'))

classifier.add(MaxPooling2D(pool_size=(2,2), strides=2))

# Flattening
classifier.add(Flatten())

# Fully connected
classifier.add(Dense(units=1024, activation='relu'))
classifier.add(Dropout(0.4))
classifier.add(Dense(units=10, activation='softmax'))

# Compile CNN
classifier.compile(optimizer=keras.optimizers.Adadelta(), loss=keras.losses.categorical_crossentropy, metrics=['accuracy'])

classifier.fit(x_train, 
               y_train,
               batch_size=128,
               epochs=12,
               verbose=1,
               validation_data=(x_test, y_test))

# Save CNN Model
classifier.save('my_model.h5') 