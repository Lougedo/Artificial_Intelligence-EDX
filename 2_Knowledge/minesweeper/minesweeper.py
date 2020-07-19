import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # Only if all of them are mines
        if self.count == len(self.cells):
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # Only if there are no known mines nearby
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            # We remove the given cell from the sentence
            self.cells.remove(cell)
            # We take one out of the mine count too
            self.count = self.count - 1
        return

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # Same as before, but we don't decrease the mine count
        if cell in self.cells:
            # We remove the given cell from the sentence
            self.cells.remove(cell)
        return


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def get_neighbours(self, cell):
        neighbours = set()
        known_mines = 0
        row, col = cell
        for i in range(row-1, row+2):
            if self.height >= i >= 0:
                for j in range(col-1, col+2):
                    if self.width >= j >= 0 and cell not in self.moves_made and (i, j) != cell:
                        if (i, j) in self.mines:
                            known_mines += 1
                        neighbours.add((i, j))
        return neighbours, known_mines

    def check_sentences_rec(self, sentences, new_sentences = list(), sentence_num = 0):
        if len(sentences) == 0 or sentence_num > len(sentences)-1: 
            return new_sentences
        actual_sentence = sentences[sentence_num]
        
        # Inferring method 1: same cells as count / no near bombs (clears sentences)
        if actual_sentence.known_mines is not None:
            for cell in actual_sentence.cells:
                self.mines.add(cell)
                sentences.remove(actual_sentence)
                self.check_sentences_rec(sentences, new_sentences, sentence_num)
        if actual_sentence.known_safes is not None:
            for cell in actual_sentence.cells:
                self.safes.add(cell)
                sentences.remove(actual_sentence)
                self.check_sentences_rec(sentences, new_sentences, sentence_num)

        # Inferring method 2: subset in the remaining sentences (adds new sentences)
        for sentence in sentences:
            if (len(sentence.cells) < len(actual_sentence.cells)):
                superset = actual_sentence
                subset = sentence
            elif (len(sentence.cells) > len(actual_sentence.cells)):
                superset = sentence
                subset = actual_sentence
            else:
                continue

            if subset.cells in superset.cells:
                new_mines = superset.mines - subset.mines
                new_cells = superset.cells - subset.cells
                new_sentences.append(Sentence(new_cells, new_mines))

        self.check_sentences_rec(sentences, new_sentences, sentence_num + 1)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Step 1
        self.moves_made.add(cell)

        # Step 2
        self.mark_safe(cell)

        # Step 3
        # We get the neighbours and the amount of known mines
        neighbours, visible_mines = self.get_neighbours(cell)
        # We use the updated number of mines (not known mines)
        new_sentence = Sentence(neighbours, count - visible_mines)
        # We add it to the knowledge base (unless, for some reason, its already on it, but it shouldn't)
        if new_sentence not in self.knowledge:
            self.knowledge.append(new_sentence)

        # Step 4
        for sentence in self.knowledge:
            mines = sentence.known_mines()
            for mine in mines:
                self.mines.add(mine) # As it is a set, duplicates are removed, so no need to check
            safes = sentence.known_safes()
            for safe in safes:
                self.safes.add(safe) # As it is a set, duplicates are removed, so no need to check

        # Step 5
        new_sentences = self.check_sentences_rec(sentences=self.knowledge)
        if new_sentences == None or len(new_sentences) == 0:
            return

        for sentence in new_sentences:
            if sentence not in self.knowledge:
                self.knowledge.append(sentence)
        while len(new_sentences) > 0:
            new_sentences = self.check_sentences_rec(sentences=self.knowledge)
            for sentence in new_sentences:
                if sentence not in self.knowledge:
                    self.knowledge.append(sentence)
                    

        return

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # Doesn't mind the element chosen as we are not looking forward to be efficient (not yet)
        if len(self.safes) == 0:
            return None
        return random.choice(tuple(self.safes))

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # We will try to look for the safest move possible (the least failure %)
        cell_chance = 1
        chosen = None
        for sentence in self.knowledge:
            failure_chance = sentence.count / len(sentence.cells) 
            if cell_chance > failure_chance:
                chosen = sentence.cells[0]
                if chosen in self.moves_made | self.mines:
                    i = 0
                    while chosen in self.moves_made | self.mines:
                        i += 1
                        chosen = sentence.cells[i]
        if chosen is None:
            for i in range(0, self.width):
                for j in range (0, self.height):
                    if (i, j) not in self.moves_made | self.mines:
                        chosen = (i, j)
                        break
        return chosen


