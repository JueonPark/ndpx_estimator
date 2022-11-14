import tensorflow as tf
import tensorflow_addons as tfa
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.utils import shuffle
# from sklearn.linear_model import LogisticRegression

from Dataset import DatasetManager
from Model import *

np.set_printoptions(precision=3, suppress=True) # for easier read

def plot_loss(history):
  plt.plot(history.history['loss'], label='loss')
  plt.plot(history.history['val_loss'], label='val_loss')
  plt.ylim([0, 300000])
  plt.xlabel('Epoch')
  plt.ylabel('Error [RealNdpxCost]')
  plt.legend()
  plt.grid(True)
  plt.tight_layout()
  plt.show()
  plt.savefig("train_loss.png")

def plot_prediction(test_predictions, test_labels):
  plt.clf()
  a = plt.axes(aspect='equal')
  plt.scatter(test_predictions, test_labels)
  plt.xlabel('Predictions [RealNdpxCost]')
  plt.ylabel('True Values [RealNdpxCost]')
  lims = [0, 1000000]
  plt.xlim(lims)
  plt.ylim(lims)
  plt.plot(lims, lims)
  plt.tight_layout()
  plt.show()
  plt.savefig("result_graph.png")


# Data to fetch from the workbook:
# [x]:
# - ShapeSize
# - #input
# - #output
# - #op
# y:
# - RealNdpxCost

# if using xlsx data
# dataset = DatasetManager.fetch_xlsx_data()
# dataset.columns = dataset.iloc[0]
# dataset = dataset[1:]

# else
dataset = DatasetManager.fetch_csv_data()

print(dataset)

# for removing N/A data
dataset = dataset.dropna()

# for shuffling dataset
dataset = shuffle(dataset)

# generate training & testing dataset & labels
train_dataset = dataset.sample(frac=0.8, random_state=1)
train_dataset = train_dataset.astype(float)
test_dataset = dataset.drop(train_dataset.index)
test_dataset = test_dataset.astype(float)

train_features = train_dataset.copy()
test_features = test_dataset.copy()

train_labels = train_features.pop('RealNdpxCost')
test_labels = test_features.pop('RealNdpxCost')

# normalizer = tf.keras.layers.Normalization(axis=-1)
# normalizer = tf.keras.layers.experimental.preprocessing.Normalization(axis=-1)
# normalizer.adapt(np.array(train_features))
# print(normalizer.mean.numpy())

# # generate model
# dnn_model = build_and_compile_model(normalizer)
dnn_model = LogisticRegression()
dnn_model.summary()

# train model
history = dnn_model.fit(
  train_features,
  train_labels,
  validation_split=0.2,
  verbose=1,
  epochs=1000)

# draw loss
plot_loss(history)

# test
test_results = {}
test_results['dnn_model'] = dnn_model.evaluate(test_features, test_labels, verbose=0)
print(test_results)

pd.DataFrame(test_results, index=['Mean absolute error [RealNdpxCost]']).T

# predictions
test_predictions = dnn_model.predict(test_features).flatten()
plot_prediction(test_predictions, test_labels)

# save model
dnn_model.save('dnn_model')
