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


def viterbi(train, test):
    '''
    TODO: implement the Viterbi algorithm.
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences with tags on the words
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    #tagset = {'ADJ','ADV','IN','PART','PRON','NUM','CONJ','UH','TO','VERB','MODAL','DET','NOUN','PERIOD','PUNCT','X'}
    tag_word = {}
    tag_tag =  {}
    initial_tag = {}
    for sentence in train:
        prev = 'START'
        #print("//////////////////////////////////////////")
        for word, tag in sentence:
            #print(word,tag)
            if tag=='START':
                continue;
            if tag not in tag_word:
                tag_word[tag] = {}
            if word not in tag_word[tag]:
                tag_word[tag][word] = 1
            else:
                tag_word[tag][word]+=1

            if prev not in tag_tag:
                tag_tag[prev] = {}
            if tag not in tag_tag[prev]:
                tag_tag[prev][tag] = 1
            else:
                tag_tag[prev][tag]+=1
            prev = tag
    laplace = 1
    tag_set = []

    idx = 0
    '''
    for key in tag_word.keys():
        print(key)
    '''


    for key,value in  tag_word.items():
        v = len(value)
        n = sum(value.values())

        for word, count in value.items():
            tag_word[key][word] = math.log((count+laplace)/(n+laplace*(v+1)))
        tag_word[key]['UNK'] = math.log(laplace/(n+laplace*(v+1)))
        tag_set.append(key)
        tag_idx_map[key] = idx
        idx+=1



    for tag1,tag2 in tag_tag.items():
        v = len(tag2)
        n = sum(tag2.values())
        n_total+=n
        for tag, count in tag2.items():
            tag_tag[tag1][tag] = math.log((count+laplace)/(n+laplace*(v+1)))
        tag_tag[tag1]['UNK'] = math.log(laplace/(n+laplace*(v+1)))

    predicts = []
    for sentence in test:
        sentence_pred = []
        n_ = len(sentence)-1
        m_ = len(tag_word)
        print(m_,n_)
        print(len(tag_set))
        trellis = [[[0,'START']]*(n_) for _ in range(m_)]

        widx = 0

        for word in sentence:
            tidx = 0
            if widx==0:
                continue;
            for cur_tag in tag_word.keys():


                #emission
                if word in tag_word[cur_tag]:
                    trellis[tidx][widx-1][0] += tag_word[cur_tag][word]
                else:
                    trellis[tidx][widx-1][0] += tag_word[cur_tag]['UNK']
                #translation

                max = float('-inf')
                max_prev_tag = tag_set[0]
                for i in range(m_):
                    if cur_tag not in tag_tag[tag_set[i]]:
                        prob = trellis[i][widx-1][0]+tag_tag[tag_set[i]]['UNK']
                    else:
                        prob = trellis[i][widx-1][0]+tag_tag[tag_set[i]][cur_tag]
                    if max<prob:
                        max = prob
                        max_prev_tag = tag_set[i]
                trellis[tidx][widx-1][0] += max
                trellis[tidx][widx-1][1] = max_prev_tag

                tidx+=1
            if widx == len(sentence)-1:
                widx_count_down = widx
                max = trellis[0][widx-1][0]
                max_tag_idx = 0
                for i in range(m_):
                    if trellis[i][widx-1][0]>max:
                        max = trellis[i][widx-1][0]
                        max_tag_idx = i
                #print(max_tag_idx)
                sentence_pred.append((sentence[widx_count_down-1],tag_set[max_tag_idx]))

                tag_pred = trellis[max_tag_idx][widx_count_down-1][1]
                widx_count_down -=1
                while widx_count_down>1:
                    sentence_pred.append((sentence[widx_count_down-1],tag_pred))
                    widx_count_down-=1
                    tag_pred = trellis[tag_idx_map[tag_pred]][widx_count_down-1][1]
                if widx_count_down == 1:
                    sentence_pred.append((sentence[1],tag_pred))
                #print(type(sentence[0]),type(tag_pred))
                sentence_pred.reverse()
                #print(type(sentence_pred))
                predicts.append(sentence_pred)
            widx+=1






    return predicts
