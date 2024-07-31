import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense
from statistics import mean
import matplotlib.pyplot as plt
import pandas as pd

import tensorflow as tf
from tensorflow.keras import layers, models,backend

#Import matrices CNN1-CNN3
try:
    from SortingData import *
except:
    pass

# Define the CNN model
def TRAINCNN(X_train,X_test,Y_train,y_test):

    model = models.Sequential()

    # Add 3D convolutional layers
    model.add(layers.Conv2D(64, kernel_size=(5, 5), activation='elu', input_shape=(51, 51, 1)))

    model.add(layers.Conv2D(64, kernel_size=(3, 3), activation='elu'))
    # Flatten the output before the fully connected layers
    model.add(layers.Flatten())

    # Add dense layers for further processing
    model.add(layers.Dense(64, activation='elu'))
  
    # Output layer for classification/regression
    model.add(layers.Dense(2))  # Deux sorties
    
    # Compile the model
    model.compile(optimizer='adagrad', loss='mae') 
    #best optimiser: adagrad

    history=model.fit(X_train, y_train, epochs=60, batch_size=1, validation_data=(X_test, y_test))

    return model,history

def plot_history(history):
  """
    Plotting training and validation learning curves.
    Args:
      history: model history with all the metric measures
  """
  fig, (ax1) = plt.subplots(1)

  # Plot loss

  ax1.set_title('Loss')
  ax1.plot(history.history['loss'], label = 'train')
  ax1.plot(history.history['val_loss'], label = 'test')
  ax1.set_ylabel('Loss')
  ax1.set_ylim(ymin=0, ymax=5)

  # Determine upper bound of y-axis
  max_loss = max(history.history['loss'] + history.history['val_loss'])

  ax1.set_xlabel('Epoch')
  ax1.legend(['Train', 'Validation'])

  plt.show()

####RUN DU CNN

datatest=TESTDATA
datatest2=TESTDATA62

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=50)

modeleCNN3,history=TRAINCNN(X_train,X_test,y_train,y_test)

loss = modeleCNN3.evaluate(X_test, y_test)
print(f"Mean Squared Error on Test Data: {loss}")
predictions = modeleCNN3.predict(datatest)
print("Predicted Positions zero (EL, AZ):")
print(predictions)
print(f"real:{DATAangle}")

predictions2 = modeleCNN3.predict(datatest2)
print("Predicted Positions zero (EL, AZ):")
print(predictions2)
print(f"real:{DATAangle2}")

predictions3 = modeleCNN3.predict(TESTDATA70)
print("Predicted Positions zero (EL, AZ):")
print(predictions3)
print(f"real:{DATAangle3}")

plot_history(history)

#SAUVEGARDE DU MODEL: CHANGER LE NOM APRES CHAQUE ESSAI
modeleCNN3.save('D:/python/CNN3_EL.keras')
