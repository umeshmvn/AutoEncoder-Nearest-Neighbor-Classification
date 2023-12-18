# -*- coding: utf-8 -*-
"""Nearest Neighbor Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QmCI3J4YGgbcbc6lr9KSaxtNUU03GYlH
"""

'''CV Programming Assignment-III'''
                                              '''PART-B'''
#Nearest Neighbor Classification
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import torch
import torchvision
from torchvision import transforms
from torchvision import datasets
from torch.utils.data import DataLoader,random_split
from torch import nn
import torch.nn.functional as F
import torch.optim as optim
from torchsummary import summary
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from collections import Counter

def loading_data():
    """Function to load and shuffle the images"""
    digits = load_digits()

    if np.random.seed(24):  # Check if the seed is set successfully
        x = digits.data
        y = digits.target

        # shuffle images
        np.random.shuffle(x)
        np.random.shuffle(y)

        return x, y
    else:
        print("Error: Failed to set seed.")
        return None, None

def l2_norm(x, y):
    """Calculate the L2 norm or the Euclidean distance between two points x and y."""
    squared_diff = np.square(x - y)
    sum_squared_diff = np.sum(squared_diff)
    euclidean_distance = np.sqrt(sum_squared_diff)
    return euclidean_distance

def nearest_neighbor(x, y, k):
    """ Predict the label of test points based on labels of k closest neighbors.
        Input: x: contains all the input images
               y: contains all the target labels
               k: number of nearest neighbors
        Outputs: pred: predictions of the test images
                y_test: labels for testing images"""

    X_train = np.concatenate([x[np.where(y == label)[0][:-50]] for label in range(10)])
    X_test = np.concatenate([x[np.where(y == label)[0][-50:]] for label in range(10)])
    y_train = np.concatenate([y[np.where(y == label)[0][:-50]] for label in range(10)])
    y_test = np.concatenate([y[np.where(y == label)[0][-50:]] for label in range(10)])

    pred = np.zeros_like(y_test)
    l2_norms = np.array([[l2_norm(X_test[i], x) for x in X_train] for i in range(len(y_test))])

    with np.nditer(l2_norms, flags=['multi_index'], op_flags=['readwrite']) as it:
        while not it.finished:
            idx = it.multi_index
            k_indices = np.argpartition(l2_norms[idx], k)[:k]
            pred[idx] = np.argmax(np.bincount(y_train[k_indices]))
            it.iternext()

    return pred, y_test

def calculate_accuracy(pred, y_test):
    """Calculate the accuracy of the Nearest Neighbor model."""
    correct_predictions = np.sum(pred == y_test)
    total_predictions = len(y_test)
    accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0.0
    return accuracy


def plot_digit_comparison(images, true_labels, predicted_labels):
    """Plot a comparison of original digits, true labels, and predicted labels."""
    fig, axes = plt.subplots(nrows=2, ncols=5, sharex=True, sharey=True, figsize=(12, 5))
    fig.suptitle("Comparison of Original Digits, True Labels, and Predicted Labels", fontsize=16)

    for i in range(10):
        ax = axes[i // 5, i % 5]

        # Plot the original digit
        ax.imshow(images[i].reshape(8, 8), cmap='gray')

        # Show the true label
        true_label = true_labels[i]
        ax.set_title(f'True: {true_label}', color='green' if true_label == predicted_labels[i] else 'blue')

        # Hide the axes
        ax.axis('off')

    plt.show()

if __name__ == '__main__':
    # Load images to run the model and get the data (x) and target (y)
    x, y = LoadingData()

    if x is not None and y is not None:
        # Creating a list of k to run the algorithm for k values of 3, 5, 7
        k = [3, 5, 7]

        # Creating a list to find the model accuracy for each value of k
        model_accuracy = []

        for val in k:
            predictions, test_labels = NearestNeighbor(x, y, val)
            accuracy = CalculateAccuracy(predictions, test_labels)
            print("Accuracy of the model with k={} nearest neighbor is {}".format(val, accuracy))
            model_accuracy.append(accuracy)

            # Plot a comparison of original digits, true labels, and predicted labels
            plot_digit_comparison(x[:10], test_labels[:10], predictions[:10])

        PlotResults(model_accuracy, k)
    else:
        print("Error: Unable to load data.")
digits = load_digits()
print(digits.data.shape)
X_train , X_test, Y_train , Y_test = train_test_split(digits.data, digits.target, test_size= 500)

print(
    f"""digits.data shape: {digits.data.shape}
X_train shape: {X_train.shape}
Y_train shape: {Y_train.shape}
X_test shape: {X_test.shape}
Y_test shape: {Y_test.shape}"""
)
class NearestNeighbor(object):
    def __init__(self):
        pass

    def train(self, X, y):
        # the nearest neighbor classifier simply remembers all the training data, without explicitly learning anything
        self.Xtr = X
        self.ytr = y

    def predict(self, X, distance='L1'):
        num_test = X.shape[0]
        Ypred = np.zeros(num_test, dtype=self.ytr.dtype)

        # loop over all test rows
        i = 0
        with np.nditer(X, flags=['multi_index'], op_flags=['readwrite']) as it:
            while not it.finished:
                row_index = it.multi_index[0]
                test_row = X[row_index, :]

                # find the nearest training image to the i'th test image
                # manhattan distance
                if distance == 'L1':
                    distances = np.sum(np.abs(self.Xtr - test_row), axis=1)

                # euclidean distance
                elif distance == 'L2':
                    distances = np.sqrt(np.sum(np.square(self.Xtr - test_row), axis=1))

                # index of nearest neighbor
                min_index = np.argmin(distances)
                # label of closest neighbor
                Ypred[row_index] = self.ytr[min_index]

                it.iternext()
                i += 1

        return Ypred
nn = NearestNeighbor()

nn.train(X_train, Y_train)
y_test_pred_L1 = nn.predict(X_test, distance='L1')
accuracy_L1 = calculate_accuracy(y_test_pred_L1, Y_test)
print('Accuracy for L1 distance = %.2f' % accuracy_L1)

nn.train(X_train, Y_train)
y_test_pred_L2 = nn.predict(X_test, distance='L2')
accuracy_L2 = calculate_accuracy(y_test_pred_L2, Y_test)
print('Accuracy for L2 distance = %.2f' % accuracy_L2)
class KNearestNeighbor(object):
    def __init__(self):
        pass

    def train(self, X, y):
        # the nearest neighbor classifier simply remembers all the training data, without explicitly learning anything
        self.Xtr = X
        self.ytr = y

    def predict(self, X, distance='L1', k=3):
        num_test = X.shape[0]
        Ypred = np.zeros(num_test, dtype=self.ytr.dtype)

        # loop over all test rows
        for i in range(num_test):
            # find the nearest training image to the i'th test image
            # manhattan distance
            if distance == 'L1':
                distances = np.sum(abs(self.Xtr - X[i, :]), axis=1)

            # euclidean distance
            if distance == 'L2':
                distances = np.linalg.norm(self.Xtr - X[i, :], axis=1)

            closest_neighbor = []
            labels = self.ytr[np.argsort(distances)].flatten()
            # label of closest k neighbors
            closest_neighbor = labels[:k]

            # returns label that is most common among k neighbors
            c = Counter(closest_neighbor)
            Ypred[i] = c.most_common(1)[0][0]

        return Ypred

kVals = np.arange(3, 20, 2)
accuracies = []

for k in kVals:
    knn = KNearestNeighbor()
    knn.train(X_train, Y_train)
    y_test_pred = knn.predict(X_test, distance='L1', k=k)
    acc = calculate_accuracy(y_test_pred, Y_test)
    accuracies.append(acc)
    print('L1 distance, K = %d' % k, 'Accuracy = %.2f' % acc)

plot_results(accuracies, kVals)

class KNearestNeighbor(object):
    def __init__(self):
        pass

    def train(self, X, y):
        # the nearest neighbor classifier simply remembers all the training data, without explicitly learning anything
        self.Xtr = X
        self.ytr = y

    def predict(self, X, distance='L1', k=3):
        num_test = X.shape[0]
        Ypred = np.zeros(num_test, dtype=self.ytr.dtype)

        # loop over all test rows
        for i in range(num_test):
            # find the nearest training image to the i'th test image
            # manhattan distance
            if distance == 'L1':
                distances = np.sum(abs(self.Xtr - X[i, :]), axis=1)

            # euclidean distance
            if distance == 'L2':
                distances = np.linalg.norm(self.Xtr - X[i, :], axis=1)

            closest_neighbor = []
            labels = self.ytr[np.argsort(distances)].flatten()
            # label of closest k neighbors
            closest_neighbor = labels[:k]

            # returns label that is most common among k neighbors
            c = Counter(closest_neighbor)
            Ypred[i] = c.most_common(1)[0][0]

        return Ypred

kVals = np.arange(3, 20, 2)
accuracies = []

for k in kVals:
    knn = KNearestNeighbor()
    knn.train(X_train, Y_train)
    y_test_pred = knn.predict(X_test, distance='L1', k=k)
    acc = calculate_accuracy(y_test_pred, Y_test)
    accuracies.append(acc)
    print('L1 distance, K = %d' % k, 'Accuracy = %.2f' % acc)

plot_results(accuracies, kVals)