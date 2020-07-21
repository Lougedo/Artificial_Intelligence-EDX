import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.

    The transition_model should return a dictionary representing the probability 
    distribution over which page a random surfer would visit next, given a corpus 
    of pages, a current page, and a damping factor.
    """
    # Total amount of pages
    number_of_pages = len(corpus) 
    # Base probability of any page, we'll have to add the rest later
    base_probability = (1 - damping_factor) / number_of_pages
    # We add the probability to all the pages and create the dict that will be returned as result
    probabilities = dict.fromkeys(corpus.keys(),base_probability)

    # Set of pages linked to the given page 
    page_links = corpus.get(page) 
    # Amount of pages linked to the given page
    number_of_page_links = len(page_links)
    # Probability of traviling to one of those pages from the given page
    if number_of_page_links > 0:
        extra_probability = damping_factor / number_of_page_links
        # We add the probability to each page
        for link in page_links:
            probabilities[link] += extra_probability
    # If there are no links, we equilibrate the probability
    else:
        probabilities = dict.fromkeys(corpus.keys(), 1/number_of_pages)

    return probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # First sample, random choice
    actual_page = random.choice(list(corpus.keys()))
    # We create the dict with same keys as the corpus and default value 0, to add later
    pagerank = dict.fromkeys(corpus.keys(), 0)
    # We calculate one time (so that we don't do it N times) the probability added each landing
    probability_added = 1 / n
    # Now we iterate N times, jumping from page to page and adding the probability in each jump
    pagerank[actual_page] += probability_added
    i = 0
    while i < n:
        # Get the transition model
        probabilities = transition_model(corpus, actual_page, damping_factor)
        # To ease its use, we get a list of values
        probabilities_values = list(probabilities.values())
        # This way, we will iterate through them and then, get a random value with a seed, depending 
        # on the range the seed ends (the list makes easier this proccess)
        index = 0
        seed = random.random()
        while seed > 0:
            seed -= probabilities_values[index]
            index += 1
        # We set the actual page to the page where the seed got to 0 or least
        actual_page = list(probabilities.keys())[index-1]
        # Add its new probability
        pagerank[actual_page] += probability_added
        # And loop again
        i += 1

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
