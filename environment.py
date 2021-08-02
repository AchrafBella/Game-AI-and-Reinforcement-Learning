import numpy as np


class Env:
    def __init__(self, dimension=(6, 7)):
        """
        this class create the game environment
        we have to respect that the first drop of peace should be in the deep
        also the game is over when one player get 4 peaces or the board left with 0 vacant column
        :param dimension: the dimension represent the board limits
        """
        self.__dimension = dimension
        self.__board = np.zeros(self.__dimension)
        self.__game_over = False
        self.__winner = None

    def drop_piece(self, row, column, piece):
        """
        A specific function for agents
        :param row:
        :param column:
        :param piece:
        :return:
        """
        if self.__board[row][column] != 0:
            row -= 1
        self.__board[row][column] = piece

    def drop_manually_piece(self, column, piece, row=5):
        """
        this function will put an element in board using the agent
        :param row:
        :param column:
        :param piece:
        :return:
        """
        if row > 6 or row < 0 or column > 7 or column < 0:
            raise Exception("Please check where you put your peace")
        if not np.any(self.__board[self.__dimension[0] - 1] == 0):
            row -= 1
        if self.__board[row][column] != 0:
            row -= 1
            raise Exception("You can't put the peace at this position")
        self.__board[row][column] = piece

    def check_game_over(self):
        """
        in this function we are going to check if all the value are full then game is over,
        :return:
        """
        if not np.any(self.__board == 0):
            self.__game_over = True
            self.__winner = 'Game is over no one won'

    def check_wining_move(self, agent):
        """
        we are going to check if there is 4 peaces vertically then game is over,
        we are going to check if there is 4 peaces  negatively sloped diagonals then game is over
        we are going to check if there is 4 peaces  positively&negatively sloped diagonals then game is over
        :param agent: the agent
        :return:
        """
        if self.__game_over:
            return

        # check vertical locations
        for r in range(self.__dimension[0] - 3):
            for c in range(self.__dimension[1]):
                if self.__board[r][c] == agent.get_piece() and self.__board[r + 1][c] == agent.get_piece() \
                        and self.__board[r + 2][c] == agent.get_piece() and self.__board[r + 3][c] == agent.get_piece():
                    self.__game_over = True
                    self.__winner = agent.get_agent_name()
                    pass
                pass
            pass

        # check horizontal location
        for r in range(self.__dimension[0]):
            for c in range(self.__dimension[1] - 3):
                if self.__board[r][c] == agent.get_piece() and self.__board[r][c + 1] == agent.get_piece() \
                        and self.__board[r][c + 2] == agent.get_piece() and self.__board[r][c + 3] == agent.get_piece():
                    self.__game_over = True
                    self.__winner = agent.get_agent_name()
                    pass
                pass
            pass

        # check negative diagonal
        for r in range(self.__dimension[0]):
            for c in range(self.__dimension[1] - 3):
                if self.__board[r][c] == agent.get_piece() and self.__board[r - 1][c + 1] == agent.get_piece() \
                        and self.__board[r - 2][c + 2] == agent.get_piece() and self.__board[r - 3][c + 3] == \
                        agent.get_piece():
                    self.__game_over = True
                    self.__winner = agent.get_agent_name()
                    pass
                pass
            pass

        # check positive diagonal
        for r in range(self.__dimension[0] - 3):
            for c in range(self.__dimension[1] - 3):
                if self.__board[r][c] == agent.get_piece() and self.__board[r + 1][c + 1] == agent.get_piece() \
                        and self.__board[r + 2][c + 2] == agent.get_piece() and self.__board[r + 3][c + 3] == \
                        agent.get_piece():
                    self.__game_over = True
                    self.__winner = agent.get_agent_name()
                    pass
                pass
            pass

        return self.__game_over

    def battle(self, agent1, agent2):
        """
        :param agent1:
        :param agent2:
        :return:
        """
        epochs = 42
        for i in range(epochs):
            if self.check_game_over():
                break
            if self.check_wining_move(agent1):
                break
            if self.check_wining_move(agent2):
                break
            row1, col1 = agent1.action(self.__board, self.__dimension)
            row2, col2 = agent2.action(self.__board, self.__dimension)

            self.drop_piece(row1, col1, agent1.get_piece())
            self.drop_piece(row2, col2, agent2.get_piece())
        return self.__winner

    def __reset_configuration(self):
        """
        :return:
        """
        self.__board = np.zeros(self.__dimension)
        self.__game_over = False
        self.__winner = None

    def run(self, agent1, agent2, rounds=100):
        """
        This function will
        :param agent1:
        :param agent2:
        :param rounds:
        :return:
        """
        agent1_pct = 0
        agent2_pct = 0
        for _ in range(rounds):
            self.__reset_configuration()
            self.battle(agent1, agent2)
            winner = self.__winner
            if winner == agent1.get_agent_name():
                agent1_pct += 1
            elif winner == agent2.get_agent_name():
                agent2_pct += 1

        print("agent: {}  percentage of winning {}%".format(agent1.get_agent_name(), (agent1_pct/rounds)*100))
        print("agent: {}  percentage of winning {}%".format(agent2.get_agent_name(), (agent2_pct/rounds)*100))

    def get_dimension(self):
        return self.__dimension

    def get_observation(self):
        return self.__board

    def get_game_state(self):
        return self.__game_over

    def get_winner(self):
        return self.__winner

    def display_env(self):
        print(*self.__board, sep='\n')
