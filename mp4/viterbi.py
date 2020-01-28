"""
This is the main entry point for MP4. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

import math
def baseline(train, test):
    '''
    TODO: implement the baseline algorithm.
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    word_tag_dict = {}
    for sentence in train:
        for word, tag in sentence:
            if word not in word_tag_dict:
                word_tag_dict[word] = {}
            if tag not in word_tag_dict[word]:
                word_tag_dict[word][tag] = 1
            else:
                word_tag_dict[word][tag]+=1

    predicts = []
    for sentence in test:
        sentence_pred = []
        for word in sentence:
            if word in word_tag_dict:
                tag_pred = max(word_tag_dict[word].keys(),key= lambda x: word_tag_dict[word][x])
                sentence_pred.append((word,tag_pred))
            else:
                sentence_pred.append((word,'NOUN'))
        predicts.append(sentence_pred)
    return predicts
    raise Exception("You must implement me")
    return predicts

def convert(alpha,count,n,v):
    return math.log((count+alpha)/(n+alpha*(v+1)))

def viterbi(train, test):
    '''
    TODO: implement the Viterbi algorithm.
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences with tags on the words
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''

    predicts = []

    tag_initial, tag_count,tag_tag,tag_word,tag_idx,tagset_len = training(train)
    for sentence in test:
        if len(sentence) == 1:
            predicts.append([('START', 'START')])
            continue
        trellis = []
        init = []
        for i in range(tagset_len):
            if sentence[1] in tag_word[i]:
                init.append(tag_initial[i] + tag_word[i][sentence[1]])
            else:
                init.append(tag_initial[i] + tag_word[i]['UNK'])
        trellis.append(init)
        path = {}
        for i in range(2, len(sentence)):
            kplus = []
            for k, tag_b in enumerate(tag_idx):
                max_prob = float('-inf')
                for j, tag_a in enumerate(tag_idx):
                    if sentence[i] in tag_word[k]:
                        prob = trellis[i - 2][j] + tag_tag[j][k] + tag_word[k][sentence[i]]
                    else:
                        prob = trellis[i - 2][j] + tag_tag[j][k] + tag_word[k]['UNK']
                    if prob > max_prob:
                        max_prob = prob
                        path[(i, tag_b)] = (i - 1, tag_a)
                kplus.append(max_prob)
            trellis.append(kplus)
        end_idx = trellis[-1].index(max(trellis[-1]))
        end_tag = list(tag_idx.keys())[end_idx]
        tag_pred = [end_tag]
        i = len(sentence) - 1
        while i > 1:
            tag_pred.append(path[(i, end_tag)][1])
            end_tag = path[(i, end_tag)][1]
            i -= 1
        tag_pred.append('START')
        tag_pred.reverse()
        sentence_pred = []
        for i in range(len(sentence)):
            temp = (sentence[i], tag_pred[i])
            sentence_pred.append(temp)
        predicts.append(sentence_pred)

    return predicts
def training(train):
    tagset = ['ADJ', 'ADV', 'IN', 'PART', 'PRON', 'NUM', 'CONJ', 'UH', 'TO', 'VERB', 'MODAL', 'DET', 'NOUN', 'PERIOD',
            'PUNCT', 'X']
    tagset_len = len(tagset)
    initial_para = 0.0001
    emission_para = 0.0001
    translation_para = 0.0001

    tag_initial = [0]*tagset_len
    tag_count = [0]*tagset_len
    tag_tag = [[0]*tagset_len for _ in range(tagset_len)]
    tag_word = [{} for _ in range(tagset_len)]
    tag_idx = {}
    for item in tagset:
        tag_idx[item] = tagset.index(item)

    for sentence in train:
        idx = 0
        for word, tag in sentence:
            if idx==0:
                idx = 1
                continue
            matched_idx = tag_idx[tag]
            if idx==1:
                tag_initial[matched_idx] += 1
            tag_count[matched_idx] += 1
            if sentence[idx - 1][0] != 'START':
                tag_tag[tag_idx[sentence[idx - 1][1]]][matched_idx] += 1
            if word in tag_word[matched_idx]:
                    tag_word[matched_idx][word] += 1
            else:
                tag_word[matched_idx][word] = 1
            idx+=1

    n = sum(tag_initial)
    v = len(tag_initial)
    for i, count in enumerate(tag_initial):
        if tag_count[i] == 0:
            tag_initial[i] = convert(initial_para,0,n,v)
        else:
            tag_initial[i] = convert(initial_para,count,n,v)

    v = tagset_len
    for i in range(len(tag_tag)):
        n= sum(tag_tag[i])
        for j in range(len(tag_tag)):
            count = tag_tag[i][j]
            if tag_count[i] == 0 or tag_count[j] == 0:
                tag_tag[i][j] = convert(translation_para,0,n,v+1)
            else:
                tag_tag[i][j] = convert(translation_para,count,n,v+1)
    for i in range(len(tag_word)):
        tag_word[i]['UNK'] = 0
        n = len(tag_word[i].keys())
        v = sum(tag_word[i].values())
        if tag_count[i] == 0:
            tag_word[i] = dict.fromkeys(tag_word[i], convert(emission_para,0,n,v+1))
        else:
            for word in tag_word[i]:
                count = tag_word[i][word]
                tag_word[i][word] = convert(emission_para,tag_word[i][word],v,n)
    return tag_initial, tag_count,tag_tag,tag_word,tag_idx,tagset_len
