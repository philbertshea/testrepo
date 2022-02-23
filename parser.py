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
NP -> N | Det N | Det NP | Det AdjP N | PP NP | AdjP N | AdjP NP | NP PP
VP -> V | V NP | V NP PP | V PP | VP PP Adv | VP Adv | VP ConjP | Adv VP
PP -> P NP
AdjP -> Adj | Adj NP
ConjP -> Conj VP | Conj NP VP
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
    wordlist = nltk.word_tokenize(sentence)
    processed = []
    for word in wordlist:
        if any(c.isalpha() for c in word):
            processed.append(word.lower())

    return processed



def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunklist = []
    for sub in tree.subtrees():
        if checktree(sub) and sub not in chunklist:
            chunklist.append(sub)
    
    return chunklist


def checktree(tree):
    subs = tree.subtrees()
    if tree.label() != 'NP':
        return False
    next(subs)
    for sub in subs:
        if sub.label() == 'NP':
            return False
        # Call checktree within itself if need to check whether NP is present within subtree of subtrees
    return True


if __name__ == "__main__":
    main()
