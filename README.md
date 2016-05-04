# Part-of-Speech Tagging
## task1
python train_hmm_tagger.py <training filename> −−\[cpostag\|postag\]
--> creates pickle file.
## task2
python hmm tagger.py <test blind filename> <output filename>
--> creates tags from blind test.
## task3
python evaluate hmm tagger.py <output filename> <test gold filename> \[cpostag\|postag\] 
--> prints out the accuracy of the tagger.
