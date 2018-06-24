import random
import pisqpipe as pp
from pisqpipe import DEBUG_EVAL, DEBUG

class Gomoku(object):
    
    def __init__(self, width, height, board = None, player = None):
        if board == None:
            board = [[0] * height] * width
        else:
            assert len(board) == width and len(board[0]) == height, 'The board does not agree with the num of rows'
        if player == None:
            player = 1
        else:
            assert player in [1,2], 'player can only be 1 or 2'
        self.height, self.width = height, width
        self.state = [board, player]

    def restart(self):
        board = [[0] * self.height] * self.width
        player = 1
        self.state = [board, player]

    def get_actions(self, parameter_list):
        # return legal actions given a state
        raise NotImplementedError
    
    def is_free(self, x, y):
        # check if a position on the board is legal given two coords
        # return True for yes, False for no
        # allow pieces other than [1,2] on the board, e.g. 3 for block
        return x >= 0 and y >= 0 and x < self.width and y < self.height and self.state[0][x][y] == 0

    def is_end(self, parameter_list):
        # check if the game has a winner given a board and a new move
        # return the winner (in [1,2]) or None for no winner
        # TODO
        pass
    
    def change_player(self):
        # change the player of the game
        if self.state[1] == 1:
            self.state[1] = 2
        elif self.state[1] == 2:
            self.state[1] = 1

    def make_move(self, x, y, player):
        # put a move to the board given two coords and a player
        # allow players other than [1,2] on the board, e.g. 3 for block
        if self.is_free(x,y):
            self.state[0][x][y] = player
            self.change_player()
        else:
            pp.pipeOut("ERROR player {} move [{},{}]".format(player, x, y))
        
    def take_back(self, x, y):
        # take a move from the board given two coords
        if x >= 0 and y >= 0 and x < self.width and y < self.height and self.state[0][x][y] != 0:
            self.state[0][x][y] = 0
            return 0
        return 2