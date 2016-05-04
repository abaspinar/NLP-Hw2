import sys

def getTestTags(outputPath):
    outputTags = []
    with open(outputPath) as f:
        for line in f.readlines():
            line = line.strip().split('|')
            outputTags.append(line[1])
    return outputTags

def getGoldenSet(goldPath, tagType=3):
    tagMode = {'cpostag': 3, 'postag': 4}
    if tagType in tagMode:
        tagType = tagMode[tagType]
    else:
        tagType = 3

    goldTags = []
    with open(goldPath) as f:
        for line in f.readlines():
            line = line.strip()
            if len(line) != 0:
                tmp = line.split()
                word = tmp[1]
                if word is not '_':
                    tag = tmp[tagType]
                    goldTags.append(tag)
    return goldTags

def accuracy(actual, predicted):
    c = 0
    for i in range(len(predicted)):
        if actual[i] == predicted[i]:
            c += 1
    return c / float(len(actual))

if __name__ == '__main__':
    argv = sys.argv[1:]
    if len(argv) < 3:
        print('Wrong number of parameters')
        sys.exit(1)
    else:
        outputPath = argv[0]
        goldPath = argv[1]
        tagType = argv[2]

        outputTags = getTestTags(outputPath)
        goldTags = getGoldenSet(goldPath, tagType)

        n_classes = {'cpostag': 14, 'postag': 24}
        if tagType in n_classes:
            tagType = n_classes[tagType]
        else:
            tagType = 14

        accur = accuracy(goldTags, outputTags)
        print(accur)


