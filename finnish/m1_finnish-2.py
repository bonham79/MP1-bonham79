#!/usr/bin/python
#To generate far, run executable ./m1_finnish.py
import pynini

##########Setting Up Vocabulary FSTs#################################################
adessive_regular = "llA"
adessive_harmony = "lla"
inessive_regular = "ssA"
inessive_harmony = "ssa"
suffixes = pynini.union("lla", "ssa", "llA", "ssA")
##Umlaut vowels are replaced with capitalized vowels due to issues between ASCII-UTF8 conversions
consonants = pynini.union("b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n","p", "q", "r", "s", "t", "v", "w", "x", "z", "S", "-")
vowels_harmony_trigger = pynini.union("u", "o", "a")
vowels_harmony_holster =  pynini.union("y", "O", "A")
vowels_neutral = pynini.union("i", "e")
vowels = pynini.union("u", "o", "a", "y", "O", "A", "i", "e")
closure_regular = pynini.union(consonants, vowels_neutral, vowels_harmony_holster).closure()
closure_harmony = pynini.union(consonants, vowels_harmony_trigger, vowels_neutral).closure()
closure = pynini.union(consonants, vowels_neutral, vowels_harmony_holster, vowels_harmony_trigger).closure()
vowels_harmony_trigger = ("u", "o", "a")
vowels_harmony_holster = ("y", "O", "A")


##FSTs to remove Umlauts and replace later respectively
regularize = (pynini.string_map([("ä", "A"), ("ö", "O"), ("š","S")]) | 
             pynini.union("b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n","p", "q", "r", "s", "t", "v", "w", "x", "z",
                         "u", "o", "a", "y", "i", "e", "-")).closure().optimize()

rvregularize = (pynini.string_map([("A", "ä"), ("O", "ö"), ("S", "š")]) | 
             pynini.union("b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n","p", "q", "r", "s", "t", "v", "w", "x", "z",
                         "u", "o", "a", "y", "i", "e", "-")).closure().optimize()



######################FST for harmony in suffix####################################################
regular_state = closure_regular.optimize()
harmony_state = closure_harmony.optimize()

adessive_regular_transduce = pynini.transducer("", adessive_regular)#, output_token_type="utf8")
adessive_harmony_transduce = pynini.transducer("", adessive_harmony)#, output_token_type="utf8")
inessive_regular_transduce = pynini.transducer("", inessive_regular)#, output_token_type="utf8")
inessive_harmony_transduce = pynini.transducer("", inessive_harmony)#, output_token_type="utf8")

transducer_adessive_harmony = harmony_state + adessive_harmony_transduce
transducer_adessive_regular = regular_state + adessive_regular_transduce
transducer_inessive_harmony = harmony_state + inessive_harmony_transduce
transducer_inessive_regular = regular_state + inessive_regular_transduce

transducer_adessive_base = transducer_adessive_regular | transducer_adessive_harmony
transducer_inessive_base = transducer_inessive_regular | transducer_inessive_harmony


###Creates arcs between harmony and regular paths to allow setting and resetting
for i in vowels_harmony_trigger:
    arc = pynini.Arc(ord(i), ord(i), 0, 5)
    transducer_adessive_base.add_arc(0, arc)
    transducer_inessive_base.add_arc(0, arc)


for i in vowels_harmony_holster:
    arc = pynini.Arc(ord(i), ord(i), 0, 0)
    transducer_adessive_base.add_arc(5, arc)
    transducer_inessive_base.add_arc(5, arc)

####Ensures regular path is default
transducer_adessive_base.set_start(0)
transducer_inessive_base.set_start(0)

transducer_adessive_base.optimize()
transducer_inessive_base.optimize()


######Morphophonemic Rules################
#Consonant Gradation rules.
double_consonants_reduce = pynini.string_map([["kk", "k"], ["pp", "p"], ["tt", "t"], ["lk", "l"], ["t", "d"]]) 
##Courtesy of http://www.lysator.liu.se/language/Languages/Finnish/Grammar.html and https://web.stanford.edu/~kiparsky/Papers/finnish.article.pdf
consonant_reduction = pynini.cdrewrite(double_consonants_reduce,  "l" | vowels | "n", vowels + suffixes, closure).optimize()

#Vowel insertion to break consonant clusters caused by suffixes
insertion = pynini.cdrewrite(pynini.transducer("", "e"), consonants, suffixes, closure).optimize()

#Finnish seems to attempt preserving morae count with /s/ as a syllabic end.  Generates a stop that assimilates 'highness' of vowel and becomes /k/
#In case this generated stop occurs after VV, it instead assimilates /s/ and becomes /t/.  Then gradation occurs due to /e/ insertion
#Similar situation seemed to occur with /s/ -> /a/ / /a/_ + suffix.  So was added to transducer.
final_stress_preservation = pynini.cdrewrite(pynini.transducer("s", "t"), vowels + (pynini.acceptor("y") | "u"), suffixes, closure) * pynini.cdrewrite(pynini.transducer("", "k"), pynini.acceptor("y") | "u", "s" + suffixes, closure) * pynini.cdrewrite(pynini.transducer("s", "a"), "a", suffixes, closure)
final_stress_preservation.optimize()

#Rule for /nt/ assimilation. 
nt_assimilation = pynini.cdrewrite(pynini.transducer("t", "n"), "n", vowels + suffixes, closure).optimize()

#Intersection of rules
transducer_adessive = regularize * transducer_adessive_base * nt_assimilation  * final_stress_preservation * insertion * consonant_reduction  * rvregularize
transducer_inessive = regularize * transducer_inessive_base * nt_assimilation  * final_stress_preservation * insertion * consonant_reduction  * rvregularize

#########################Generates FAR ###############################3
with pynini.Far("finnish.far", "w") as sink:
    sink["ADESSIVE"] = transducer_adessive
    sink["INESSIVE"] = transducer_inessive
