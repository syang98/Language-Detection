"""
Author: Steven Yang
This is the network to detect Languages: Spanish, French, Dutch
"""
import numpy as np
import random
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
import keras.optimizers


number_letters = 126
number_labels = 3

data = np.load("test_data.npy")
random.shuffle(data)
# break up data
n = len(data)
data_1 = data[:n//2]
data_2 = data[n//2:]

data_1 = data_1.astype(np.float64)
data_2 = data_2.astype(np.float64)

total = data_1 + data_2
X = total[:, 0:126]
Y = total[:, 126]
print(X.shape)
# Scale X and Y
standard_scaler = preprocessing.StandardScaler().fit(X)
scaled_X = standard_scaler.transform(X)
scaled_Y = keras.utils.to_categorical(Y, num_classes=number_labels)
print(scaled_Y.shape)
train_X, test_X, train_Y, test_Y = train_test_split(scaled_X, scaled_Y, test_size=.2, random_state=42)


print("model time")
# DNN
model = Sequential()
model.add(Dense(500, input_dim=126, kernel_initializer="glorot_uniform", activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(300, kernel_initializer="glorot_uniform", activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(100, kernel_initializer="glorot_uniform", activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(number_labels, kernel_initializer="glorot_uniform", activation="softmax"))
model_optimizer = keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
model.compile(loss='categorical_crossentropy', optimizer=model_optimizer, metrics=['accuracy'])
model.fit(train_X, train_Y, epochs=6, batch_size=128, validation_split=0.10, shuffle=True)


scores = model.evaluate(test_X, test_Y, verbose=1)
print("acc: ", scores[1])

