import pickle
from Spritesheet import *

# reading from pickle file
def unpickle(filename):
    infile = open(filename,'rb')
    data = pickle.load(infile)
    infile.close()
    return data

data = unpickle('levels/level1')
print(data)