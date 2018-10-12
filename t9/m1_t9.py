import pynini
import string

##Vocabulary
lm_char = pynini.Fst.read("t9.char.lm")
lm_word = pynini.Fst.read("t9.word.lm")
t9 = pynini.transducer("0","[32]")  
t9_relations = ["0", "1", "2abc", "3def", "4ghi", "5jkl", "6mno", "7pqrs", "8tuv", "9wxyz"]

##Reading vocabulary into alphabet.
for i in range(10):
    for k in t9_relations[i]:
        t9 = pynini.union(pynini.transducer(str(i),str(k)), t9)
##Adding punctuation to vocabulary        
for i in string.punctuation:
    t9 = t9 | pynini.transducer("1", "[" + str(ord(i)) + "]")
##Closure and optimization
t9.closure().optimize()
##Inverstion for decoding
encoder = pynini.invert(t9).optimize()

def encode(message):
    return (message.lower() * encoder).stringify()


def decode(message):
###performs encoding on message, projects pathways to intersect with character ngram
###Then returns most likely path
    lattice = (message * t9).project(True) * lm_char 
    return pynini.shortestpath(lattice).stringify()