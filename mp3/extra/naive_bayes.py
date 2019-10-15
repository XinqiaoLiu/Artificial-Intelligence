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
    lamda = 0.5
    pos_dict = {}
    pos_sum = 0
    neg_dict = {}
    neg_sum = 0
    pos_review = 0
    for i in range(len(train_set)):
        if (train_labels[i]==1):
            pos_review+=1
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

    pos_prior = pos_review/len(train_set)

    for key,value in pos_dict.items():
        pos_dict[key] = math.log((value+smoothing_parameter)/(pos_sum+smoothing_parameter*(v+1)))

    for key,value in neg_dict.items():
        neg_dict[key] = math.log((value+smoothing_parameter)/(neg_sum+smoothing_parameter*(v+1)))

    predicted = []
    pos_unknown = math.log(smoothing_parameter/(pos_sum+smoothing_parameter*(v+1)))
    neg_unknown = math.log(smoothing_parameter/(neg_sum+smoothing_parameter*(v+1)))

    bi_pos_dict = {}
    bi_pos_sum = 0
    bi_neg_dict = {}
    bi_neg_sum = 0
    for i in range(len(train_set)):
        if (train_labels[i]==1):
            for j in range(len(train_set[i])-1):
                bw = train_set[i][j]+train_set[i][j+1]
                bi_pos_sum+=1
                if bw in bi_pos_dict:
                    bi_pos_dict[bw]+=1
                else:
                    bi_pos_dict[bw] = 1

        else:
            for j in range(len(train_set[i])-1):
                bw = train_set[i][j]+train_set[i][j+1]
                bi_neg_sum+=1
                if bw in bi_neg_dict:
                    bi_neg_dict[bw] += 1
                else:
                    bi_neg_dict[bw] =1
    bv= len(bi_pos_dict)+len(bi_neg_dict)
    bi_smoothing_parameter = 0.01
    for key,value in bi_pos_dict.items():
        bi_pos_dict[key] = math.log((value+bi_smoothing_parameter)/(bi_pos_sum+bi_smoothing_parameter*(v+1)))

    for key,value in bi_neg_dict.items():
        bi_neg_dict[key] = math.log((value+bi_smoothing_parameter)/(bi_neg_sum+bi_smoothing_parameter*(v+1)))


    bi_pos_unknown = math.log(bi_smoothing_parameter/(bi_pos_sum+bi_smoothing_parameter*(v+1)))
    bi_neg_unknown = math.log(bi_smoothing_parameter/(bi_neg_sum+bi_smoothing_parameter*(v+1)))


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

        bi_pos_p = 0
        bi_neg_p = 0
        for j in range(len(dev_set[i])-1):
            bw = dev_set[i][j]+dev_set[i][j+1]
            if bw in bi_pos_dict:
                bi_pos_p+=bi_pos_dict[bw]
            else:
                bi_pos_p+=bi_pos_unknown
            if bw in bi_neg_dict:
                bi_neg_p+=bi_neg_dict[bw]
            else:
                bi_neg_p+=bi_neg_unknown
        bi_pos_p+=math.log(pos_prior)
        bi_neg_p+=math.log(1-pos_prior)

        pos_p = (1-lamda)*math.exp(pos_p) + lamda*math.exp(bi_pos_p)
        neg_p = (1-lamda)*math.exp(neg_p) + lamda*math.exp(bi_neg_p)

        if(pos_p>=neg_p):
            predicted.append(1)
        else:
            predicted.append(0)
    return predicted
