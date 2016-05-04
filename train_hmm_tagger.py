import argparse
import pickle

def train(trainPath, tagType):
    tagMode = {'cpostag': 3, 'postag': 4}
    if tagType in tagMode:
        tagType = tagMode[tagType]
    else:
        tagType = 3
    tag = '<begin>'
    trans = {}
    emiss = {}
    tags = {}
    lastTag = '<finish>'
    with open(trainPath) as f:
        for line in f.readlines():
            line = line.strip()
            if len(line) == 0:
                tr = tag + '_' + lastTag
                trans[tr] = trans.get(tr, 0) + 1
                tag = '<begin>'
            else:
                tmp = line.split()
                word = tmp[1]
                if word is not '_':
                    curTag = tmp[tagType]
                    tr = tag + '_' + curTag
                    em = tag + '_' + word
                    trans[tr] = trans.get(tr, 0) + 1
                    emiss[em] = emiss.get(em, 0) + 1
                    tags[curTag] = tags.get(curTag, 0) + 1
                    tag = curTag
    return tags, trans, emiss

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("training_filepath")
    parser.add_argument("-c", "--cpostag", action="store_true")
    parser.add_argument("-p", "--postag", action="store_true")
    args = parser.parse_args()
    if args.cpostag:
        tagType = 'cpostag'
    elif args.postag:
        tagType = 'postag'
    trainDataPath = args.training_filepath

    pickle.dump(train(trainDataPath, tagType), open('trainingDictionary.txt','wb'))


