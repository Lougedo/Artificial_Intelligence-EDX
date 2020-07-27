import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP 
S -> VP NP 
S -> VP
S -> S Conj S

NP -> N
NP -> NP AP
NP -> AP NP
NP -> Det NP
NP -> Det Adj NP

VP -> V
VP -> V AP
VP -> V NP
VP -> V PP
VP -> V NP PP

PP -> P NP
PP -> P NP AP
PP -> PP PP

AP -> Adv 
AP -> Adj AP
AP -> Adj
"""


grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():
    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    alphabetic_characters = 'abcdefghijklmnopqrstuvwxyz'
    tokens = nltk.word_tokenize(sentence.lower())
    # Remove any word without alphabetic characters
    for word in tokens:
        remove = True
        for letter in word:
            if letter in alphabetic_characters:
                remove = False
        if remove is True:
            tokens.remove(word)
    return tokens


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    NPs = list()
    subtrees = tree.subtrees()
    
    for subtree in subtrees:
        if subtree.label() == "N":
            NPs.append(subtree)
    
    return NPs



if __name__ == "__main__":
    main()
