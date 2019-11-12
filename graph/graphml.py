
import os, nltk, os.path, re, string
import argparse
from nltk.stem.porter import PorterStemmer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

factory = StemmerFactory()
stemmer = factory.create_stemmer()

def hanya_huruf (input):
    r = re.match('^[a-zA-Z]+$',input)
    if r==None:
        return False
    else:
        return True

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--infile', default='', help = 'input filename')
    parser.add_argument('-o','--outfile', default='', help = 'output filename')
    return parser.parse_args()

args = parse_args()
outfile = args.outfile
infile = args.infile

filename = open('tweets-bpjs.txt','r')
fcontent = filename.read()
filename.close()

outText = open('tweets-bpjs-graph.graphml','w')

outText.write(
    '<?xml version="1.0" encoding="UTF-8"?> \n <graphml xmlns="http://graphml.graphdrawing.org/xmlns"> \n <key id="d0" for="edge" attr.name="weight" attr.type="double"/> \n <graph id="G" edgedefault="undirected">')

fs = fcontent.split()
stemmed = []
wordlist = []

for word in fs:
    if hanya_huruf(word) and len(word)<15 and len(word)>1 and word!='Iing' :
        word = stemmer.stem(word).lower()
        if word not in nltk.corpus.stopwords.words('english') :
            if word not in nltk.corpus.stopwords.words('indonesian'):
                stemmed.append(word)
                if word not in wordlist:
                    wordlist.append(word)
                    outText.write('<node id="' + word + '"/>' + '\n')
                else:
                    pass
            else:
                pass

ls = len(stemmed)

counter = -1
pairlist = []
pairlistnodupes = []

for word in stemmed:
    pl = stemmed.index(word)
    if pl < ls:
        adjword1 = stemmed[pl + 1]
        adjword2 = stemmed[pl + 2]
        adjword3 = stemmed[pl + 3]
        adjword4 = stemmed[pl + 4]
        pair1 = 'source="' + word + '" target="' + adjword1
        pairlist.append(pair1)
        pair2 = 'source="' + word + '" target="' + adjword2
        pairlist.append(pair2)
        pair3 = 'source="' + word + '" target="' + adjword3
        pairlist.append(pair3)
        pair4 = 'source="' + word + '" target="' + adjword4
        pairlist.append(pair4)
    else:
        print
        'stems done'

for pair in pairlist:
    counter = counter + 1
    occur = pairlist.count(pair)
    if occur > 1:
        if pair not in pairlistnodupes:
            pairlistnodupes.append(pair)
    else:
        outText.write('<edge id="' + str(counter) + '" ' + pair + '"><data key="d0"></data></edge>' + '\n')

for pair in pairlistnodupes:
    counter = counter + 1
    occur = pairlist.count(pair)
    outText.write(
        '<edge id="' + str(counter) + '" ' + pair + '"><data key="d0">' + str(occur) + '.0</data></edge>' + '\n')

outText.write('  </graph></graphml>')
outText.close()
print
'done'
