# -*- coding: utf-8 -*-
"""3ModelANN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pSCf4gU1XE5M2j0j6lhBqh4_qsFrkfgy
"""

import tensorflow as tf

# Load the CIFAR-10 dataset
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()

# Normalize the pixel values
x_train = x_train / 255.0
x_test = x_test / 255.0

# Convert the labels to one-hot encoded vectors
num_classes = 10
y_train = tf.keras.utils.to_categorical(y_train, num_classes)
y_test = tf.keras.utils.to_categorical(y_test, num_classes)

import tensorflow as tf
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras import Model

# Define the CNN model architecture
class CNNModel(Model):
  def __init__(self):
    super(CNNModel, self).__init__()
    self.conv1 = Conv2D(32, 3, activation='relu')
    self.maxpool1 = MaxPooling2D()
    self.conv2 = Conv2D(64, 3, activation='relu')
    self.maxpool2 = MaxPooling2D()
    self.conv3 = Conv2D(128, 3, activation='relu')
    self.maxpool3 = MaxPooling2D()
    self.flatten = Flatten()
    self.dense1 = Dense(128, activation='relu')
    self.dense2 = Dense(num_classes, activation='softmax')

  def call(self, x):
    x = self.conv1(x)
    x = self.maxpool1(x)
    x = self.conv2(x)
    x = self.maxpool2(x)
    x = self.conv3(x)
    x = self.maxpool3(x)
    x = self.flatten(x)
    x = self.dense1(x)
    return self.dense2(x)

# Instantiate the CNN model
model1 = CNNModel()

# Compile the model
model1.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
hist = model1.fit(x_train, y_train, epochs=10, validation_data=(x_test, y_test))

import matplotlib.pyplot as plt
import numpy as np

from sklearn.metrics import classification_report

# Get the predicted class labels for the test set
y_pred = model1.predict(x_test)
y_pred_classes = np.argmax(y_pred, axis=1)

# Get the true class labels for the test set
y_true = np.argmax(y_test, axis=1)

# Define the class names
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 
               'dog', 'frog', 'horse', 'ship', 'truck']

# Generate the classification report
print(classification_report(y_true, y_pred_classes, target_names=class_names))

# Evaluate the model on the test set
loss, accuracy = model1.evaluate(x_test, y_test)

print(f"Test loss: {loss:.2f}")
print(f"Test accuracy: {accuracy:.2f}")

# Plot the training and validation loss and accuracy
epochs = range(1, len(hist.history['accuracy']) + 1)

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(epochs, hist.history['loss'], 'bo', label='Training loss')
plt.plot(epochs, hist.history['val_loss'], 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(epochs, hist.history['accuracy'], 'bo', label='Training accuracy')
plt.plot(epochs, hist.history['val_accuracy'], 'b', label='Validation accuracy')
plt.title('Training and validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

plt.show()

from sklearn.metrics import confusion_matrix
# Generate the confusion matrix
cm = confusion_matrix(y_true, y_pred_classes)

# Plot the confusion matrix
plt.figure(figsize=(8, 8))
plt.imshow(cm, cmap=plt.cm.Blues)
plt.title("Confusion matrix")
plt.xlabel("Predicted labels")
plt.ylabel("True labels")
plt.xticks(range(num_classes))
plt.yticks(range(num_classes))
plt.colorbar()

plt.show()

import tensorflow as tf
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras import Model

# Load the pre-trained VGG16 model
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(32, 32, 3))

# Freeze the base model layers
for layer in base_model.layers:
  layer.trainable = False

# Add new layers on top of the base model
x = Flatten()(base_model.output)
x = Dense(256, activation='relu')(x)
output = Dense(num_classes, activation='softmax')(x)
model2 = Model(inputs=base_model.input, outputs=output)

# Compile the model
model2.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
hist1 = model2.fit(x_train, y_train, epochs=5, validation_data=(x_test, y_test))

import matplotlib.pyplot as plt
import numpy as np

# Evaluate the model on the test set
loss, accuracy = model2.evaluate(x_test, y_test)

print(f"Test loss: {loss:.2f}")
print(f"Test accuracy: {accuracy:.2f}")

# Plot the training and validation loss and accuracy
epochs = range(1, len(hist1.history['accuracy']) + 1)

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(epochs, hist1.history['loss'], 'bo', label='Training loss')
plt.plot(epochs, hist1.history['val_loss'], 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(epochs, hist1.history['accuracy'], 'bo', label='Training accuracy')
plt.plot(epochs, hist1.history['val_accuracy'], 'b', label='Validation accuracy')
plt.title('Training and validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

plt.show()

from sklearn.metrics import confusion_matrix

# Get the predicted class labels for the test set
y_pred2 = model2.predict(x_test)
y_pred_classes2 = np.argmax(y_pred2, axis=1)

# Get the true class labels for the test set
y_true2 = np.argmax(y_test, axis=1)

# Generate the confusion matrix
cm = confusion_matrix(y_true2, y_pred_classes2)

# Plot the confusion matrix
plt.figure(figsize=(8, 8))
plt.imshow(cm, cmap='magma')
plt.title("Confusion matrix")
plt.xlabel("Predicted labels")
plt.ylabel("True labels")
plt.xticks(range(num_classes))
plt.yticks(range(num_classes))
plt.colorbar()

plt.show()

# Generate the classification report
print(classification_report(y_true2, y_pred_classes2, target_names=class_names))

# Define the MLP model architecture
model3 = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(32, 32, 3)),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])

# Compile the model
model3.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
history3 = model3.fit(x_train, y_train, epochs=10, validation_data=(x_test, y_test))

# Evaluate the model on the test set
test_loss, test_acc = model3.evaluate(x_test, y_test)
print('Test accuracy:', test_acc)

print(classification_report(np.argmax(y_test, axis=-1), y_pred3, target_names=target_names))

from sklearn.metrics import classification_report

# Get the predicted class labels for the test set
y_pred3 = model3.predict(x_test)
y_pred_classes3 = np.argmax(y_pred3, axis=1)

# Get the true class labels for the test set
y_true3 = np.argmax(y_test, axis=1)

# Generate the classification report
print(classification_report(y_true3, y_pred_classes3, target_names=class_names))

# Plot the training and validation loss and accuracy
epochs = range(1, len(history3.history['accuracy']) + 1)

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(epochs, history3.history['loss'], 'bo', label='Training loss')
plt.plot(epochs, history3.history['val_loss'], 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(epochs, history3.history['accuracy'], 'bo', label='Training accuracy')
plt.plot(epochs, history3.history['val_accuracy'], 'b', label='Validation accuracy')
plt.title('Training and validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

plt.show()

from sklearn.metrics import confusion_matrix
# Generate the confusion matrix
cm = confusion_matrix(y_true3, y_pred_classes3)

# Plot the confusion matrix
plt.figure(figsize=(8, 8))
plt.imshow(cm, cmap="plasma")
plt.title("Confusion matrix")
plt.xlabel("Predicted labels")
plt.ylabel("True labels")
plt.xticks(range(num_classes))
plt.yticks(range(num_classes))
plt.colorbar()

plt.show()