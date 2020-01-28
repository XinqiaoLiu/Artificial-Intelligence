# perceptron.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/27/2018
import numpy as np

from numpy import array
from numpy.linalg import norm
"""
This is the main entry point for MP5. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

def classify(train_set, train_labels, dev_set, learning_rate,max_iter):
    """
    train_set - A Numpy array of 32x32x3 images of shape [7500, 3072].
                This can be thought of as a list of 7500 vectors that are each
                3072 dimensional.  We have 3072 dimensions because there are
                each image is 32x32 and we have 3 color channels.
                So 32*32*3 = 3072
    train_labels - List of labels corresponding with images in train_set
    example: Suppose I had two images [X1,X2] where X1 and X2 are 3072 dimensional vectors
             and X1 is a picture of a dog and X2 is a picture of an airplane.
             Then train_labels := [1,0] because X1 contains a picture of an animal
             and X2 contains no animals in the picture.

    dev_set - A Numpy array of 32x32x3 images of shape [2500, 3072].
              It is the same format as train_set
    """
    # TODO: Write your code here
    # return predicted labels of development set

    w = [0]*len(train_set[0])
    b = 0
    for iter in range(max_iter):
        for i in range(len(train_set)):
            x = train_set[i]
            sum = np.dot(x,w)
            pred = np.sign(sum+b)
            if pred<0:
                pred = 0
            if pred!=train_labels[i]:
                w = w+learning_rate*(train_labels[i]-pred)*x
                b = b+learning_rate*(train_labels[i]-pred)

    pred_lables = []
    for i in range(len(dev_set)):
        x = dev_set[i]
        sum = np.dot(x,w)
        if np.sign(sum+b) <0:
            pred_lables.append(0)
        else:
            pred_lables.append(1)

    return pred_lables

def classifyEC(train_set, train_labels, dev_set,learning_rate,max_iter):
    # Write your code here if you would like to attempt the extra credit
    k = 1
    pred = []
    for i in range(len(dev_set)):

        dist=[norm(dev_set[i]-train) for train in train_set]
        idx = np.argpartition(dist, k)[:k]
        sum_ = 0
        for j in idx:
            sum_+=train_labels[j]
        if sum_>=k/2:
            pred.append(1)
        else:
            pred.append(0)
    return pred
