"""
This is the main entry point for MP4. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
import math
import numpy as np
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


def viterbi(train, test):
    '''
    TODO: implement the Viterbi algorithm.
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences with tags on the words
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''

    tags = ['ADJ', 'ADV', 'IN', 'PART', 'PRON', 'NUM', 'CONJ', 'UH', 'TO', 'VERB', 'MODAL', 'DET', 'NOUN', 'PERIOD',
            'PUNCT', 'X']
    tags_idx = {tags[i]: i for i in range(len(tags))}

    init_smoothing = 0.001
    emission_smoothing = 0.001
    trans_smoothing = 0.001

    predicts = []

    tag_occr_at_beginning = [0 for i in range(len(tags))]
    tag_occr = [0 for i in range(len(tags))]
    tag_paris_occr = [[0 for i in range(len(tags))] for j in range(len(tags))]
    tag_word_pairs_occr = [{} for i in range(len(tags))]

    for sentence in train:

        tag_occr_at_beginning[tags_idx[sentence[1][1]]] += 1
        for i, (word, tag) in enumerate(sentence):
            if i > 0:
                tag_occr[tags_idx[tag]] += 1
                if sentence[i - 1][0] != 'START':
                    tag_paris_occr[tags_idx[sentence[i - 1][1]]][tags_idx[tag]] += 1
                if word in tag_word_pairs_occr[tags_idx[tag]].keys():
                    tag_word_pairs_occr[tags_idx[tag]][word] += 1
                else:
                    tag_word_pairs_occr[tags_idx[tag]][word] = 1

    total_tag_occr_beginning = sum(tag_occr_at_beginning)
    for i, num in enumerate(tag_occr_at_beginning):
        if tag_occr[i] == 0:
            tag_occr_at_beginning[i] = np.NINF
            continue
        tag_occr_at_beginning[i] = np.log(
            (num + init_smoothing) / (total_tag_occr_beginning + init_smoothing * len(tag_occr_at_beginning)))
    for i in range(len(tag_paris_occr)):
        total_i_tag_pairs = sum(tag_paris_occr[i])
        for j in range(len(tag_paris_occr)):
            if tag_occr[i] == 0 or tag_occr[j] == 0:
                tag_paris_occr[i][j] = np.NINF
                continue
            tag_paris_occr[i][j] = np.log((tag_paris_occr[i][j] + trans_smoothing) / (total_i_tag_pairs + trans_smoothing*len(tags)))
    for i in range(len(tag_word_pairs_occr)):
        tag_word_pairs_occr[i]['UNKNOWN'] = 0
        if tag_occr[i] == 0:
            tag_word_pairs_occr[i] = dict.fromkeys(tag_word_pairs_occr[i], np.NINF)
            continue
        total_i_tag_word = sum(tag_word_pairs_occr[i].values())
        for word in tag_word_pairs_occr[i]:
            tag_word_pairs_occr[i][word] = np.log((tag_word_pairs_occr[i][word] + emission_smoothing) / (total_i_tag_word + emission_smoothing*len(tag_word_pairs_occr[i].keys())))

    for sentence in test:
        if len(sentence) == 1:
            predicts.append([('START', 'START')])
            continue
        trellis = []
        init = []
        for i in range(len(tags)):
            if sentence[1] in tag_word_pairs_occr[i].keys():
                init.append(tag_occr_at_beginning[i] + tag_word_pairs_occr[i][sentence[1]])
            else:
                init.append(tag_occr_at_beginning[i] + tag_word_pairs_occr[i]['UNKNOWN'])
        trellis.append(init)
        path = {}
        for i in range(2, len(sentence)):
            time_next = []
            for k, tag_b in enumerate(tags_idx):
                max_prob = np.NINF
                for j, tag_a in enumerate(tags_idx):
                    if sentence[i] in tag_word_pairs_occr[k].keys():
                        prob = trellis[i - 2][j] + tag_paris_occr[j][k] + tag_word_pairs_occr[k][sentence[i]]
                    else:
                        prob = trellis[i - 2][j] + tag_paris_occr[j][k] + tag_word_pairs_occr[k]['UNKNOWN']
                    if prob > max_prob:
                        max_prob = prob
                        path[(i, tag_b)] = (i - 1, tag_a)
                time_next.append(max_prob)
            trellis.append(time_next)
        last_tag_idx = trellis[-1].index(max(trellis[-1]))
        last_tag = list(tags_idx.keys())[last_tag_idx]
        predicted_tags = [last_tag]
        i = len(sentence) - 1
        while i > 1:
            predicted_tags.append(path[(i, last_tag)][1])
            last_tag = path[(i, last_tag)][1]
            i -= 1
        predicted_tags.append('START')
        predicted_tags.reverse()
        predicted_sentence = []
        for i in range(len(sentence)):
            temp = (sentence[i], predicted_tags[i])
            predicted_sentence.append(temp)
        predicts.append(predicted_sentence)

    return predicts
