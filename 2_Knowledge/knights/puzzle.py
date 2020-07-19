from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

basic_knowledge = And(
    # Nobody can be both
    Not(And(AKnave, AKnight)),
    Not(And(BKnave, BKnight)),
    Not(And(CKnave, CKnight)),
    # But has to be one
    Or(AKnight, AKnave), 
    Or(BKnight, BKnave),
    Or(CKnight, CKnave))

# Puzzle 0
# A says "I am both a knight and a knave."
sentence_0A = And(AKnave, AKnight)

knowledge0 = And(
    basic_knowledge,
    Biconditional(AKnight, sentence_0A))

# Puzzle 1
# A says "We are both knaves."
sentence_1A = And(BKnave, AKnave)
# B says nothing.

knowledge1 = And(
    basic_knowledge,
    Biconditional(AKnight, sentence_1A))

# Puzzle 2
# A says "We are the same kind."
sentence_2A = And(
    Or(
        And(AKnave, BKnave),
        And(AKnight, BKnight)))
# B says "We are of different kinds."
sentence_2B = And(
    Or(
        And(AKnave, BKnight),
        And(AKnight, BKnave)))

knowledge2 = And(
    basic_knowledge,
    Biconditional(AKnight, sentence_2A),
    Biconditional(BKnight, sentence_2B))

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
sentence_3A = Or(
        AKnight,
        AKnave)
# B says "A said 'I am a knave'."     <-- I'm understanding B says that A literally said that,
# B says "C is a knave."                  and not that A says B is a knave
sentence_3B = And(
    Biconditional(AKnight, AKnave),
    CKnave)
# C says "A is a knight."
sentence_3C = AKnight

knowledge3 = And(
    basic_knowledge,
    Biconditional(AKnight, sentence_3A),
    Biconditional(BKnight, sentence_3B),
    Biconditional(CKnight, sentence_3C))


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
