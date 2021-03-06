from collections import deque
import glob
import json
import numpy as np
import os.path as osp

# 乱数シードを設定
np.random.seed(30)



class Lang:
    def __init__(self, name):
        self.name = name
        self.word2index = {}
        self.word2count = {}
        self.index2word = {0: "SOS", 1: "EOS"}
        self.n_words = 2  # Count SOS and EOS

    def addSentence(self, sentence):
        for word in sentence.split(' '):
            self.addWord(word)

    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1





def prepareData(lang1, lang2, root_dir='__data_example/data', max_length=10, copy_num=5, reverse=False):
    input_lang, output_lang, pairs = readLangs(lang1, lang2, root_dir, max_length, copy_num, reverse)
    print("Read %s sentence pairs" % len(pairs))
    # pairs = filterPairs(pairs)
    print("Trimmed to %s sentence pairs" % len(pairs))
    print("Counting words...")
    for pair in pairs:
        input_lang.addSentence(pair[0])
        output_lang.addSentence(pair[1])
    print("Counted words:")
    print(input_lang.name, input_lang.n_words)
    print(output_lang.name, output_lang.n_words)
    return input_lang, output_lang, pairs


def readLangs(lang1, lang2, root_dir='../', max_length=10, copy_num=5, reverse=False):
    print("Reading jsons...")

    page_tags_arr = deque()
    reg_json_path = osp.join(root_dir, '*.json')
    json_files = glob.glob(reg_json_path)
    # print(json_files)
    for file in json_files:
        # Read the file and split into lines
        with open(file, 'r') as f:
            page_tags_arr.append(json.load(f))   # , encoding='utf-8'

    # Split every line into pairs and normalize
    print(page_tags_arr[0])
    pairs = shuffle_tags(page_tags_arr, max_length, copy_num)

    # Reverse pairs, make Lang instances
    if reverse:
        pairs = [list(reversed(p)) for p in pairs]
        input_lang = Lang(lang2)
        output_lang = Lang(lang1)
    else:
        input_lang = Lang(lang1)
        output_lang = Lang(lang2)

    return input_lang, output_lang, pairs


def shuffle_tags(page_tags_arr, max_length=10, copy_num=5):
    shuffled_page_tags_arr_list = []
    for page_tags in page_tags_arr:
        # shuffled_page_tags_arr_list.append(deque())
        N = int(len(page_tags) / max_length) + 2
        srcs = list(np.array_split(page_tags, N))
        for _ in range(copy_num):
            for src in srcs:
                # copy_num 分、シャッフルして増やす。
                src = src.copy()
                shuffled = src.copy()
                np.random.shuffle(shuffled)
                shuffled_page_tags_arr_list.append((' '.join(shuffled), ' '.join(src)))
                # print(shuffled_page_tags_arr_list)
                try:
                    assert len(src) < max_length
                except:
                    print(page_tags)
                    print(len(page_tags), len(src), N)
                    assert len(src) < max_length
        #     print(srcs)
        # break

    print(len(shuffled_page_tags_arr_list),      #=>  dataset = [pairs1, pairs2, pairs3, ... ]
            len(shuffled_page_tags_arr_list[1]),    #=>  pairs = [pair1, pair2, pair3, ...]
            len(shuffled_page_tags_arr_list[2][0]),   #=>  pair = [["formula ref /ref ..."], ["formula ref /ref ..."]]
            len(shuffled_page_tags_arr_list[2][0]),)   #=>  = "formula ref /ref /formula formula formula /ref /formula ref"
    print(shuffled_page_tags_arr_list[1][0])
    return shuffled_page_tags_arr_list


