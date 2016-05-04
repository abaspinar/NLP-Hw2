import pickle
from collections import defaultdict as ddict
import sys

def viterbi(sentence, tags, transition, emission):
    probs = ddict(lambda: ddict(lambda: -1))
    probs[-1]['<begin>'] = 1.0
    backpt = ddict(lambda: {})
    i = -1
    for i, word in enumerate(sentence):
        for tag, cur_count in tags.items():
            path_probs = {}
            if i == 0:
                prev_tag = '<begin>'
                tr = prev_tag+'_'+tag
                if tr in transition:
                    trans = float(transition[tr])
                else:
                    trans = -1
                em = tag+'_'+word
                if em in emission:
                    emiss = float(emission[em])/cur_count
                else:
                    emiss = -1
                path_probs[tag] = (probs[i-1][prev_tag] * trans * emiss)
            else:
                for prev_tag, prev_count in tags.items():
                    tr = prev_tag+'_'+tag
                    if tr in transition:
                        trans = float(transition[tr])/prev_count
                    else:
                        trans = -1
                    em = tag+'_'+word
                    if em in emission:
                        emiss = float(emission[em])/cur_count
                    else:
                        emiss = -1
                    path_probs[prev_tag] = (probs[i-1][prev_tag] * trans * emiss)
            best_tag = max(path_probs, key=path_probs.get)
            probs[i][tag] = path_probs[best_tag]
            backpt[i][tag] = best_tag
    i += 1
    for tag, cur_count in tags.items():
        tr = tag + '_' + '<finish>'
        if tr in transition:
            trans = float(transition[tr])/cur_count
        else:
            trans = -1
        emiss = 1
        path_probs[tag] = (probs[i-1][tag] * trans * emiss)
        best_tag = max(path_probs, key=path_probs.get)
        probs[i][tag] = path_probs[best_tag]
        backpt[i][tag] = best_tag

    currrent_tag = max(probs[i], key=probs[i].get)
    predicted_tags = []
    for j in range(i,-1,-1):
        predicted_tags.append(currrent_tag)
        currrent_tag = backpt[j][currrent_tag]
    predicted_tags.reverse()
    return predicted_tags[:-1]

def getTestData(blindPath):
    sentences = []
    with open(blindPath) as f:
        sentence = []
        for line in f.readlines():
            line = line.strip()
            if len(line) == 0:
                sentences.append(sentence)
                sentence = []
            else:
                tmp = line.split()
                word = tmp[1]
                if word is not '_':
                    sentence.append(word)
    if len(sentence) > 0:
        sentences.append(sentence)
    return sentences

if __name__ == '__main__':
    argv = sys.argv[1:]
    if len(argv) < 2:
        print('Wrong number of parameters')
        sys.exit(1)
    else:
        testPath = argv[0]
        outputPath = argv[1]

        tags, trans, emiss = pickle.load(open('trainingDictionary.txt','rb'))
        sentences = getTestData(testPath)

        pos_tags = [viterbi(sentence, tags, trans, emiss) for sentence in sentences]
        with open(outputPath,'w') as f:
            for i, sentence in enumerate(sentences):
                for j, word in enumerate(sentence):
                    f.writelines('%s|%s\n' % (word, pos_tags[i][j]))

