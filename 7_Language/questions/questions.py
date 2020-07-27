import nltk
from nltk.tokenize import RegexpTokenizer
import sys
import os
import string
import math
from num2words import num2words

FILE_MATCHES = 1
SENTENCE_MATCHES = 2


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = dict()
    corpus_path = os.path.join(".", directory)
    corpus_files = os.listdir(corpus_path)

    # I'm assuming all are txt. If not, simple IF will do the filtering
    for txt in corpus_files:
        string_file = ""
        with open(os.path.join(corpus_path, txt)) as f:
            string_file = f.read()
        files[txt] = string_file

    return files

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokenizer = RegexpTokenizer(r'\w+')
    stopwords = nltk.corpus.stopwords.words("english")
    lemmatizer = nltk.wordnet.WordNetLemmatizer()
    stemmer = nltk.stem.SnowballStemmer('english')
    # Get lowercase and rid of apostrophes
    text = document.lower().replace("\n", " ").replace("”", " ").replace("“", " ").replace(" ’", " ").replace(" ‘", " ")

    # Get rid of punctuation and uppercase
    tokens = tokenizer.tokenize(text)
    # Get rid of stopwords
    for word in tokens:
        if word in stopwords:
            tokens.remove(word)
    
    # Get rid of single characters
    for word in tokens:
        if len(word) < 2:
            tokens.remove(word)
    
    # Convert numbers to text [Not using it as it leaves phrases as words, should check]
    """for word in tokens:
        if word.isnumeric():
            tokens[tokens.index(word)] = num2words(word)"""


    # Lemmatize words 
    for word in tokens:
        tokens[tokens.index(word)] = lemmatizer.lemmatize(word)

    # Stem words
    for word in tokens:
        tokens[tokens.index(word)] = stemmer.stem(word)

    return tokens


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    words = dict()
    for doc in documents:
        tokens = documents[doc]
        checked_words = set()
        for word in tokens:
            if word in checked_words:
                continue
            if word in words:
                words[word] += 1
                checked_words.add(word)
            else:
                words[word] = 1
                checked_words.add(word)
    for word in words:
        # idf(t) = log(NumberOfDocs/(DocsAppearing))
        words[word] = math.log(len(documents) / words[word])

    return words


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    # TF-IDF = NumberOfAppearencesInDocument * IDF_Value
    tf_idf = dict()
    for document in files:
        tf_idf[document] = 0
        tokens = files[document]
        for word in query:
            if idfs.get(word) is None:
                continue
            appeareances = 0
            for token in tokens:
                if word == token:
                    appeareances += 1
            tf_idf[document] += (appeareances * idfs[word])

    tf_idf = sorted(tf_idf.items(), key=lambda x: x[1], reverse=True)
    result = list()
    for document in range (0, n):
        result.append(tf_idf[document][0])
    return result


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    matches = dict()
    for sentence in sentences:
        match_counter = total_counter = idf_counter = 0
        idf_counted_words = set()
        for word in sentences[sentence]:
            total_counter += 1
            if word in query:
                match_counter += 1
                if word not in idf_counted_words:
                    idf_counter += idfs[word]
                    idf_counted_words.add(word)
        # We save idf count and density, in case its needed
        if idf_counter != 0 and match_counter/total_counter != 0:
            matches[sentence] = (idf_counter, match_counter / total_counter)

    matches = sorted(matches.items(), key=lambda x: x[1], reverse=True)
    result = list()
    for document in range (0, n):
        result.append(matches[document][0])
    return result

if __name__ == "__main__":
    main()
