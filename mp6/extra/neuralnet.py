# neuralnet.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/29/2019
"""
This is the main entry point for MP6. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

import numpy as np
import torch, os
from torch import nn
from torch import optim
import torch.utils.data as Data


class NeuralNet(torch.nn.Module):
    def __init__(self, lrate,loss_fn,in_size,out_size):
        """
        Initialize the layers of your neural network

        @param lrate: The learning rate for the model.
        @param loss_fn: A loss function defined in the following way:
            @param yhat - an (N,out_size) tensor
            @param y - an (N,) tensor
            @return l(x,y) an () tensor that is the mean loss
        @param in_size: Dimension of input
        @param out_size: Dimension of output

        For Part 1 the network should have the following architecture (in terms of hidden units):

        in_size -> 32 ->  out_size

        """
        super(NeuralNet, self).__init__()
        self.loss_fn = loss_fn
        self.lrate = lrate
        self.in_size = in_size
        self.out_size = out_size
        self.hidden1 = nn.Sequential(nn.Conv2d(3,6,5),nn.BatchNorm2d(6),nn.ELU(),nn.MaxPool2d(3,stride=1),nn.Dropout(p=0.3),\
        nn.Conv2d(6,3,5),nn.BatchNorm2d(3),nn.ELU(),nn.MaxPool2d(3,stride=1),nn.Dropout(p=0.5))
        self.hidden2 = nn.Sequential(nn.Linear(1200,128),nn.LayerNorm(128),nn.ELU(), nn.Linear(128,64),nn.LayerNorm(64), nn.ELU(), nn.Linear(64,64), nn.ELU(),nn.Linear(64,out_size))
        # self.optimizer = optim.Adam(self.parameters(),lrate,weight_decay=0.05)
        self.optimizer = optim.Adam(self.parameters(),lrate)
    def set_parameters(self, params):
        """ Set the parameters of your network
        @param params: a list of tensors containing all parameters of the network
        """
        tmp = ['self.hidden1.0.weight', 'self.hidden1.0.bias', 'self.hidden1.1.weight', 'self.hidden1.1.bias', 'self.hidden1.1.running_mean', 'self.hidden1.1.running_var', 'self.hidden1.1.num_batches_tracked', 'self.hidden1.4.weight', 'self.hidden1.4.bias', 'self.hidden1.5.weight', 'self.hidden1.5.bias', 'self.hidden1.5.running_mean', 'self.hidden1.5.running_var', 'self.hidden1.5.num_batches_tracked', 'self.hidden2.0.weight', 'self.hidden2.0.bias', 'self.hidden2.1.weight', 'self.hidden2.1.bias', 'self.hidden2.3.weight', 'self.hidden2.3.bias', 'self.hidden2.5.weight', 'self.hidden2.5.bias']
        for i in range(len(tmp)):
            tmp[i] = params[i]

    def get_parameters(self):
        """ Get the parameters of your network
        @return params: a list of tensors containing all parameters of the network
        """
        return_value = []
        for i in self.state_dict():
            return_value.append(self.state_dict()[i])
        return return_value


    def forward(self, x):
        """ A forward pass of your neural net (evaluates f(x)).

        @param x: an (N, in_size) torch tensor

        @return y: an (N, out_size) torch tensor of output from the network
        """
        reshapedX = torch.reshape(x, (-1,32,32,3))
        x = reshapedX.permute(0,3,1,2)
        tmp1 = self.hidden1(x)
        tmp2 = torch.reshape(tmp1, (-1,1200))
        return_value =  self.hidden2(tmp2)

        return return_value

    def step(self, x,y):
        """
        Performs one gradient step through a batch of data x with labels y
        @param x: an (N, in_size) torch tensor
        @param y: an (N,) torch tensor
        @return L: total empirical risk (mean of losses) at this time step as a float
        """
        yhat = self.forward(x)
        loss = self.loss_fn(yhat,y)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.item()



def fit(train_set,train_labels,dev_set,n_iter,batch_size=100):
    """ Make NeuralNet object 'net' and use net.step() to train a neural net
    and net(x) to evaluate the neural net.

    @param train_set: an (N, in_size) torch tensor
    @param train_labels: an (N,) torch tensor
    @param dev_set: an (M,) torch tensor
    @param n_iter: int, the number of epochs of training
    @param batch_size: The size of each batch to train on. (default 100)

    # return all of these:

    @return losses: Array of total loss at the beginning and after each iteration. Ensure len(losses) == n_iter
    @return yhats: an (M,) NumPy array of binary labels for dev_set
    @return net: A NeuralNet object

    # NOTE: This must work for arbitrary M and N
    """
    lrate = 0.0001
    loss_fn = nn.CrossEntropyLoss()
    in_size = train_set.shape[1]
    out_size = 2
    net = NeuralNet(lrate,loss_fn,in_size,out_size)

    # if os.path.exists('net.model'):
    #     net = torch.load('net.model')
    #
    # net.set_parameters(net.get_parameters())

    data = Data.TensorDataset(train_set,train_labels)
    data_loader = torch.utils.data.DataLoader(dataset = data, batch_size = batch_size, shuffle = True)
    return_loss = []
    for i in range(n_iter):
        total_loss = 0
        for x,y in data_loader:
            total_loss += net.step(x,y)
        print(total_loss)
        return_loss.append(total_loss)
    net.eval()
    yhat = net(dev_set)
    yhat_list = []
    # print(yhat)
    for i in range(len(yhat)):
        if(yhat[i][0]>yhat[i][1]):
            yhat_list.append(0)
        else:
            yhat_list.append(1)
    return return_loss,yhat_list,net
