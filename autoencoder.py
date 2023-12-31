# -*- coding: utf-8 -*-
"""Autoencoder.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YKJN9P-uRz1B7G3DkoY_YhoLrXetMLgC
"""

'''CV Programming Assignment-III'''
                                                    '''PART-A'''
#Autoencoder using fully connected layers
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

# Convert data to torch.FloatTensor
transform = transforms.Compose([transforms.ToTensor()])

# Load the training and test datasets
train_data = datasets.MNIST(root='data', train=True, download=True, transform=transform)
test_data = datasets.MNIST(root='data', train=False, download=True, transform=transform)

# Create training and test dataloaders
# Number of subprocesses to use for data loading
num_workers = 2
# How many samples per batch to load
batch_size = 10

# Prepare data loaders
train_loader = torch.utils.data.DataLoader(train_data, batch_size=batch_size, shuffle=True, num_workers=num_workers)
test_loader = torch.utils.data.DataLoader(test_data, batch_size=batch_size, shuffle=False, num_workers=num_workers)

# Example code to iterate through a batch and visualize images
dataiter = iter(test_loader)
images, labels = next(dataiter)

# Plot the first 10 images in the batch
fig, axes = plt.subplots(1, 10, figsize=(20, 2))

for i, ax in enumerate(axes):
    ax.imshow(np.squeeze(images[i]), cmap='gray')
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

plt.show()
import torch
import torch.nn as nn
import torch.optim as optim

class AutoencoderFC(nn.Module):
    def __init__(self):
        super(AutoencoderFC, self).__init__()

        # Define the size of the encoded layer
        encoded_size = 32
        layer_sizes = [1*28*28, 256, 128, encoded_size]

        # Create Encoder layers using a for loop
        encoder_layers = []
        for i in range(len(layer_sizes) - 1):
            encoder_layers.append(nn.Linear(layer_sizes[i], layer_sizes[i+1]))
            encoder_layers.append(nn.ReLU())
        self.encoderFC = nn.Sequential(*encoder_layers)

        # Create Decoder layers using a for loop
        decoder_sizes = layer_sizes[::-1]  # Reverse the layer sizes for the decoder
        decoder_layers = []
        for i in range(len(decoder_sizes) - 1):
            decoder_layers.append(nn.Linear(decoder_sizes[i], decoder_sizes[i+1]))
            decoder_layers.append(nn.ReLU())
        decoder_layers.append(nn.Linear(decoder_sizes[-1], 1*28*28))
        decoder_layers.append(nn.Sigmoid())  # Applied sigmoid to the output for pixel values between 0 and 1
        self.decoderFC = nn.Sequential(*decoder_layers)

    def forward(self, x):
        x = self.encoderFC(x)
        x = self.decoderFC(x)
        return x

# Create an instance of the AutoencoderFC model
model = AutoencoderFC()
print(model)

# Validation using MSE Loss function
loss_function = nn.MSELoss()

# Using an Adam Optimizer with lr = 0.001
optimizer = optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-8)

epochs = 10
outputs = []
losses = []

for epoch in range(epochs):
    train_loss = 0.0
    for image, _ in train_loader:
        # Reshaping the image to (-1, 784)
        image = image.view(-1, 28*28)

        # Output of Autoencoder
        with torch.set_grad_enabled(True):
            reconstructed = model(image)

            # Calculating the loss function
            loss = loss_function(reconstructed, image)

            # The gradients are set to zero,
            # the gradient is computed and stored.
            # .step() performs parameter update
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        train_loss += loss.item() * image.size(0)

    train_loss = train_loss / len(train_loader)
    losses.append(train_loss)
    print('Epoch: {} \tTraining Loss: {:.6f}'.format(epoch, train_loss))
    outputs.append((epoch, image, reconstructed))
plt.plot(losses, label='training loss')
plt.legend()
import matplotlib.pyplot as plt
import numpy as np

# Assuming you have already imported necessary libraries and defined your model and test_loader

dataiter = iter(test_loader)

# Assuming batch_size is defined somewhere in your code
batch_size = test_loader.batch_size

for i in range(10):
    # obtain one batch of test images
    images, labels = next(dataiter)
    images_flatten = images.view(images.size(0), -1)

    # get sample outputs
    output = model(images_flatten)

    # prep images for display
    images = images.numpy()

    # output is resized into a batch of images
    output = output.view(batch_size, 1, 28, 28)

    # use detach when it's an output that requires_grad
    output = output.detach().numpy()

    # plot the first ten input images and then reconstructed images
    fig, axes = plt.subplots(nrows=2, ncols=10, sharex=True, sharey=True, figsize=(25, 4))

    # input images on the top row, reconstructions on the bottom
    for images, row in zip([images, output], axes):
        for img, ax in zip(images, row):
            ax.imshow(np.squeeze(img), cmap='gray')
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)

plt.show()

import matplotlib.pyplot as plt
import numpy as np

# Assuming you have already imported necessary libraries and defined your model and test_loader

dataiter = iter(test_loader)

# Assuming batch_size is defined somewhere in your code
batch_size = test_loader.batch_size

for i in range(10):
    # obtain one batch of test images
    images, labels = next(dataiter)
    images_flatten = images.view(images.size(0), -1)

    # get sample outputs
    with torch.no_grad():
        output = model(images_flatten)

    # prep images for display
    images = images.numpy()

    # output is resized into a batch of images
    output = output.view(batch_size, 1, 28, 28)

    # use detach when it's an output that requires_grad
    with torch.no_grad():
        output = output.detach().numpy()

    # plot the first ten input images and then reconstructed images
    fig, axes = plt.subplots(nrows=2, ncols=10, sharex=True, sharey=True, figsize=(25, 4))

    # input images on the top row, reconstructions on the bottom
    for images, row in zip([images, output], axes):
        for img, ax in zip(images, row):
            ax.imshow(np.squeeze(img), cmap='gray')
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)

plt.show()

# Convolutional Autoencoder
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import numpy as np

# Define the Autoencoder CNN class
class AutoencoderCNN(nn.Module):
    def __init__(self):
        super(AutoencoderCNN, self).__init__()

        # Encoder
        self.encoderCNN = nn.Sequential(
            nn.Conv2d(1, 16, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(16, 8, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )

        # Decoder
        self.decoderCNN = nn.Sequential(
            nn.ConvTranspose2d(8, 8, 2, stride=2),
            nn.ReLU(),
            nn.ConvTranspose2d(8, 16, 2, stride=2),
            nn.ReLU(),
            nn.ConvTranspose2d(16, 1, 1, stride=1),
            nn.Sigmoid()
        )

    def forward(self, x):
        x = self.encoderCNN(x)
        x = self.decoderCNN(x)
        return x

# Initialize the model
model = AutoencoderCNN()

# Loss function and optimizer
loss_function = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-8)

# Load the MNIST dataset
transform = transforms.Compose([transforms.ToTensor()])
mnist_trainset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
train_loader = DataLoader(mnist_trainset, batch_size=64, shuffle=True)

# Training the model
epochs = 10
losses = []
for epoch in range(epochs):
    train_loss = 0.0
    for images, _ in train_loader:
        optimizer.zero_grad()
        reconstructed = model(images)
        loss = loss_function(reconstructed, images)
        loss.backward()
        optimizer.step()
        train_loss += loss.item() * images.size(0)
    train_loss = train_loss / len(train_loader.dataset)
    losses.append(train_loss)
    print(f'Epoch: {epoch+1}, Training Loss: {train_loss:.6f}')

# Plot training losses
plt.plot(losses, label='Training Loss')
plt.legend()
plt.show()

# Visualize some reconstructed images
def visualize_reconstruction(model, data_loader, num_images=10):
    model.eval()
    images, _ = next(iter(data_loader))
    with torch.no_grad():
        reconstructed = model(images)
    images = images.numpy()[:num_images]
    reconstructed = reconstructed.numpy()[:num_images]

    fig, axes = plt.subplots(nrows=2, ncols=num_images, figsize=(20, 4))
    for idx in range(num_images):
        axes[0, idx].imshow(np.squeeze(images[idx]), cmap='gray')
        axes[0, idx].axis('off')
        axes[1, idx].imshow(np.squeeze(reconstructed[idx]), cmap='gray')
        axes[1, idx].axis('off')
    plt.show()

visualize_reconstruction(model, train_loader)