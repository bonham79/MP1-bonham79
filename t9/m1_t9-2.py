#!/usr/bin/pytho
###Improved T9 decoder that is biased towards word strings due to intersection with word trasducer

####
#####To execute, run executable with either arguments (str) or (str, str))
####Feeding only a single argument will run decoder function as if string is T9 encoded
####Feeding two strings, with second str = "e" will run a T9 encoded on first string and return encoded function.

import pynini
import string
import sys
##Vocabulary
lm_char = pynini.Fst.read("t9.char.lm.4")
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
    return (message.lower() @ encoder).stringify()

def decode(message):
###performs encoding on message, projects pathways to intersect with character ngram
###Then returns most likely path
    lattice = ((message * t9).project(True) @ lm_char) @ lm_word  
    return pynini.shortestpath(lattice).stringify()

def main():
    if len(sys.argv[1:]) == 0:
        raise Exception("Lack of arguments.  Please provide either a string or string-bool pair.")
    if len(sys.argv[1:]) == 1:
        message = sys.argv[1]
        print(decode(message))
    if len(sys.argv[1:]) == 2:
        message = sys.argv[1]
        function = sys.argv[2]
        assert(function == "e")
        print(encode(message))
    if len(sys.argv[1:]) > 2:
        raise Exception("Too many arguments. Please provide either a string or string-bool pari.")

if __name__ == "__main__":
    main()
