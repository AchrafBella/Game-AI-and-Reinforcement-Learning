import random
import numpy as np
from operator import itemgetter
import itertools as it


class Agent:
    """"
    this agent represent a simple a approach that consist of using the hazard
    i call this the random agent
    """
    def __init__(self, agent_name, piece):
        self.agent_name = agent_name
        self.piece = piece
        pass

    def get_piece(self):
        return self.piece

    def get_agent_name(self):
        return self.agent_name

    def action(self, observation, dimension):
        """
        :param observation:
        :param dimension
        :return:
        """
        columns = list()
        for col_ in range(dimension[1]):
            if observation[0][col_] == 0:
                columns.append(col_)
        col = random.choice(columns)
        for row in reversed(range(dimension[0])):
            if observation[row][col] == 0:
                print("row:", row, "col:", col, self.piece)
                return row, col


class HeuristicAgent:
    """
    this agent will use a heuristic that make choose wisely the place of piece by looking all the vacant
    places around and a sign a specific score for each possible place
    """
    def __init__(self, agent_name, piece):
        self.agent_name = agent_name
        self.piece = piece
        pass

    def get_piece(self):
        return self.piece

    def get_agent_name(self):
        return self.agent_name

    def get_patterns(self, observation, pairs):
        """
        this function will get the patterns for the move for each move will assign a specific score
        :param observation:
        :param pairs:
        :return:
        """
        last_row = 5
        last_col = 6
        first_col = 0
        scores = list()
        for pair in pairs:
            if pair[0] == last_row or pair[1] == last_col:
                # check the left
                if observation[pair[0]][pair[1]-1] == self.get_piece():
                    score = 100
                    scores.append((pair, score))
            elif pair[0] == last_row or pair[1] == first_col:
                # check only the right
                if observation[pair[0]][pair[1]+1] == self.get_piece():
                    score = 101
                    scores.append((pair, score))
                    pass
                pass
            elif pair[1] == last_col:
                # check only the left, diagonal and the down
                if observation[pair[0]][pair[1]-1] == self.get_piece() or observation[pair[0]-1][pair[1]] == \
                        self.get_piece() or observation[pair[0]+1][pair[1]-1] == self.get_piece():
                    score = 102
                    scores.append((pair, score))
                    pass
                pass
            elif pair[1] == first_col:
                # check only the right, diagonal and the down
                if observation[pair[0]][pair[1]+1] == self.get_piece() or observation[pair[0]-1][pair[1]] == \
                        self.get_piece() or observation[pair[0]+1][pair[1]+1] == self.get_piece():
                    score = 103
                    scores.append((pair, score))
                    pass
                pass
            else:
                # check left, right both diagonal and down
                if observation[pair[0]][pair[1]-1] == self.get_piece() or observation[pair[0]][pair[1]+1] == \
                        self.get_piece() or observation[pair[0]+1][pair[1]-1] == self.get_piece() or \
                        observation[pair[0]+1][pair[1]-1] == self.get_piece() or observation[pair[0]-1][pair[1]]:
                    score = 104
                    scores.append((pair, score))
                    pass
                pass
        return scores

    @staticmethod
    def action(observation, dimension=None):
        if np.all(observation == 0):
            return 5, random.randint(0, 6)
        vacant_places = np.argwhere(observation == 0)
        s_vacant_places = sorted(vacant_places, key=itemgetter(1))
        gs = it.groupby(s_vacant_places, key=itemgetter(1))
        valid_moves = [max(v, key=itemgetter(0)) for k, v in gs]
        return valid_moves
