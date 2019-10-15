# naive_bayes.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018

"""
This is the main entry point for MP4. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
import math
def naiveBayes(train_set, train_labels, dev_set, smoothing_parameter, pos_prior):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
              It follows the same format as train_set

    smoothing_parameter - The smoothing parameter you provided with --laplace (1.0 by default)
    """
    # TODO: Write your code here
    # return predicted labels of development set
    pos_dict = {}
    pos_sum = 0
    neg_dict = {}
    neg_sum = 0
    for i in range(len(train_set)):
        if (train_labels[i]==1):
            for w in train_set[i]:
                pos_sum+=1
                if w in pos_dict:
                    pos_dict[w]+=1
                else:
                    pos_dict[w] = 1

        else:
            for w in train_set[i]:
                neg_sum+=1
                if w in neg_dict:
                    neg_dict[w] += 1
                else:
                    neg_dict[w] =1
    v= len(pos_dict)+len(neg_dict)

    for key,value in pos_dict.items():
        pos_dict[key] = math.log((value+smoothing_parameter)/(pos_sum+smoothing_parameter*(v+1)))

    for key,value in neg_dict.items():
        neg_dict[key] = math.log((value+smoothing_parameter)/(neg_sum+smoothing_parameter*(v+1)))

    predicted = []
    pos_unknown = math.log(smoothing_parameter/(pos_sum+smoothing_parameter*(v+1)))
    neg_unknown = math.log(smoothing_parameter/(neg_sum+smoothing_parameter*(v+1)))
    for i in range(len(dev_set)):
        pos_p = 0
        neg_p = 0
        for w in dev_set[i]:
            if w in pos_dict:
                pos_p+=pos_dict[w]
            else:
                pos_p+=pos_unknown
            if w in neg_dict:
                neg_p+=neg_dict[w]
            else:
                neg_p+=neg_unknown
        pos_p+=math.log(pos_prior)
        neg_p+=math.log(1-pos_prior)
        if(pos_p>=neg_p):
            predicted.append(1)
        else:
            predicted.append(0)
    return predicted
