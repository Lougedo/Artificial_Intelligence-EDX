import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def parent_prob(people, one_gene, two_genes, parent):
    if parent in one_gene:
        return (1 - PROBS['mutation']) * 0.5
    elif parent in two_genes:
        return 1 - PROBS['mutation']
    else:
        return PROBS['mutation']


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    probability = 1.0
    """For example, if the family consists of Harry, James, and Lily, then calling this function 
    where one_gene = {"Harry"}, two_genes = {"James"}, and trait = {"Harry", "James"} should 
    calculate the probability that Lily has zero copies of the gene, Harry has one copy of the 
    gene, James has two copies of the gene, Harry exhibits the trait, James exhibits the trait, 
    and Lily does not exhibit the trait."""
    # Considerations: 
        # I'm assuming people can only be in one group, if else it would be nonsense
        # I'm treating people with only one listed parent as if there were no listed parents
    for person in people.values():
        mother = person['mother']
        father = person['father']
        mother_prob = parent_prob(people, one_gene, two_genes, mother)
        father_prob = parent_prob(people, one_gene, two_genes, father)
        if person['name'] in one_gene:
            genes_amount = 1
            if mother is None or father is None:
                probability *= PROBS['gene'][1]
            else:
                # Probability of getting one gene from either of both parents but not both
                probability *= (mother_prob * (1 - father_prob)) + (father_prob * (1- mother_prob))
        elif person['name'] in two_genes:
            genes_amount = 2
            if mother is None or father is None:
                probability *= PROBS['gene'][2]
            else:
                probability *= mother_prob * father_prob
        elif person['name'] not in one_gene.union(two_genes):
            genes_amount = 0
            if mother is None or father is None:
                probability *= PROBS['gene'][0]
            else:
                probability *= (1 - mother_prob) * (1 - father_prob)
        if person['name'] in have_trait:
            probability *= PROBS['trait'][genes_amount][True]
        else:
            probability *= PROBS['trait'][genes_amount][False]
    return probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person_prob in probabilities:
        if person_prob in one_gene:
            probabilities[person_prob]['gene'][1] += p
        elif person_prob in two_genes:
            probabilities[person_prob]['gene'][1] += p
        else:
            probabilities[person_prob]['gene'][1] += p

        if person_prob in have_trait:
            probabilities[person_prob]['trait'][True] += p
        else:
            probabilities[person_prob]['trait'][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        total_prob = 0.0
        # We first get the total
        for genes_amount in range(3):
            total_prob += probabilities[person]['gene'][genes_amount]
        # And then update it to be 1
        for genes_amount in range(3):
            probabilities[person]['gene'][genes_amount] /= total_prob
        total_prob = 0.0
        # We first get the total
        for genes_amount in probabilities[person]['trait']:
            total_prob += probabilities[person]['trait'][genes_amount]
        # And then update it to be 1
        for genes_amount in probabilities[person]['trait']:
            probabilities[person]['trait'][genes_amount] /= total_prob


if __name__ == "__main__":
    main()
