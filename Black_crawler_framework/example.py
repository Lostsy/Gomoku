import random
import pisqpipe as pp
from pisqpipe import DEBUG_EVAL, DEBUG

pp.infotext = 'name="pbrain-pyrandom", author="Jan Stransky", version="1.0", country="Czech Republic", www="https://github.com/stranskyjan/pbrain-pyrandom"'

MAX_BOARD = 20
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]


def brain_init():
	if pp.width < 5 or pp.height < 5:
		pp.pipeOut("ERROR size of the board")
		return
	if pp.width > MAX_BOARD or pp.height > MAX_BOARD:
		pp.pipeOut("ERROR Maximal board size is {}".format(MAX_BOARD))
		return
	pp.pipeOut("OK")

def brain_restart():
	for x in range(pp.width):
		for y in range(pp.height):
			board[x][y] = 0
	pp.pipeOut("OK")

def isFree(x, y):
	return x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] == 0

def brain_my(x, y):
	if isFree(x,y):
		board[x][y] = 1
	else:
		pp.pipeOut("ERROR my move [{},{}]".format(x, y))

def brain_opponents(x, y):
	if isFree(x,y):
		board[x][y] = 2
	else:
		pp.pipeOut("ERROR opponents's move [{},{}]".format(x, y))

def brain_block(x, y):
	if isFree(x,y):
		board[x][y] = 3
	else:
		pp.pipeOut("ERROR winning move [{},{}]".format(x, y))

def brain_takeback(x, y):
	if x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] != 0:
		board[x][y] = 0
		return 0
	return 2

def brain_turn():
	if pp.terminateAI:
		return
	i = 0
	while True:
		x = random.randint(0, pp.width)
		y = random.randint(0, pp.height)
		i += 1
		if pp.terminateAI:
			return
		if isFree(x,y):
			break
	if i > 1:
		pp.pipeOut("DEBUG {} coordinates didn't hit an empty field".format(i))
	pp.do_mymove(x, y)

def brain_end():
	pass

def brain_about():
	pp.pipeOut(pp.infotext)

if DEBUG_EVAL:
	import win32gui
	def brain_eval(x, y):
		# TODO check if it works as expected
		wnd = win32gui.GetForegroundWindow()
		dc = win32gui.GetDC(wnd)
		rc = win32gui.GetClientRect(wnd)
		c = str(board[x][y])
		win32gui.ExtTextOut(dc, rc[2]-15, 3, 0, None, c, ())
		win32gui.ReleaseDC(wnd, dc)


class Gomoku(object):

	def __init__(self, width, height, board=None, player=None):
		if board == None:
			board = [[0 for i in range(height)] for j in range(width)]
		else:
			assert len(board) == width and len(board[0]) == height, 'The board does not agree with the num of rows'
		if player == None:
			player = 1
		else:
			assert player in [1, 2], 'player can only be 1 or 2'
		self.height, self.width = height, width
		self.state = [board, player]

	def restart(self):
		board = [[0 for i in range(self.height)] for j in range(self.width)]
		player = 1
		self.state = [board, player]

	def is_free(self, x, y):
		# check if a position on the board is legal given two coords
		# return True for yes, False for no
		# allow pieces other than [1,2] on the board, e.g. 3 for block
		return x >= 0 and y >= 0 and x < self.width and y < self.height and self.state[0][x][y] == 0

	def is_occupied(self, x, y):
		# check if a position on the board is occupied given two coords
		# return True for yes, False for no
		# allow pieces other than [1,2] on the board, e.g. 3 for block
		return x >= 0 and y >= 0 and x < self.width and y < self.height and self.state[0][x][y] != 0

	def is_end(self, x, y, player):
		# check if the game has a winner given a board and a new move
		# return the winner (in [1,2]) or None for no winner
		# check x axis
		cross = ""
		for i in range(max(0, x - 4), min(MAX_BOARD, x + 5)):
			cross += str(self.state[0][i][y])
		if cross.find(str(player) * 5):
			return [player]
		# check y axis
		cross = ""
		for i in range(max(0, y - 4), min(MAX_BOARD, y + 5)):
			cross += str(self.state[0][x][i])
		if cross.find(str(player) * 5):
			return [player]
		# check \
		cross = ""
		for i in range(max(0, x - 4), min(MAX_BOARD, x + 5)):
			cross += str(self.state[0][i][y + (x - i)])
		if cross.find(str(player) * 5):
			return [player]
		# check /
		cross = ""
		for i in range(max(0, y - 4), min(MAX_BOARD, y + 5)):
			cross += str(self.state[0][x - y + i][i])
		if cross.find(str(player) * 5):
			return [player]


	def change_player(self):
		# change the player of the game
		if self.state[1] == 1:
			self.state[1] = 2
		elif self.state[1] == 2:
			self.state[1] = 1

	def make_move(self, x, y, player):
		# put a move to the board given two coords and a player
		# allow players other than [1,2] on the board, e.g. 3 for block
		if self.is_free(x, y):
			self.state[0][x][y] = player
			self.change_player()
		else:
			pp.pipeOut("ERROR player {} move [{},{}]".format(player, x, y))

	def take_back(self, x, y):
		# take a move from the board given two coords
		self.state[0][x][y] = 0

	def get_board(self):
		return self.state[0]

	def get_player(self):
		return self.state[1]



def GA(gomoku):
	CHECK_SCOPE = 2#the range para

	def round_check(board,x, y, scope):
		# given a position (x,y) and scope(integer), check the positions around and return a position list that can make a move.
		position = []
		for i in range(max(0,x-scope),min(x+scope+1,MAX_BOARD)):
			for j in range(max(0,y-scope),min(y+scope+1,MAX_BOARD)):
				if board[i][j] ==0:
					position.append((i,j))
		return


	def position2check(board):
		p2c = []
		board = gomoku.state[0]
		for i in range(MAX_BOARD):
			for j in range(MAX_BOARD):
				if board[i][j] != 0:
					rounds = round_check(board,i,j,CHECK_SCOPE)
					for item in rounds:
						if item not in p2c:
							p2c.append(item)
		return p2c

	def fitness_function(para):
		#the function to compute a position's fitness value
		pass

	def cross_fertilize(para):
		#the cross_fertilize function to create new gomoku chains
		pass

	def mutation(para):
		#the mutation to create mutation of gomoku chains with a motation rate
		pass

	def selectionofgod_the_programmer(para):
		#given chains and theri fitness values, make a simulation of natural selection, return a list of new selected gomoku chains
		pass



######################################################################
# A possible way how to debug brains.
# To test it, just "uncomment" it (delete enclosing """)
######################################################################
'''
# define a file for logging ...
DEBUG_LOGFILE = "/tmp/pbrain-pyrandom.log"
# ...and clear it initially
with open(DEBUG_LOGFILE,"w") as f:
	pass

# define a function for writing messages to the file
def logDebug(msg):
	with open(DEBUG_LOGFILE,"a") as f:
		f.write(msg+"\n")
		f.flush()

# define a function to get exception traceback
def logTraceBack():
	import traceback
	with open(DEBUG_LOGFILE,"a") as f:
		traceback.print_exc(file=f)
		f.flush()
	raise

# use logDebug wherever
# use try-except (with logTraceBack in except branch) to get exception info
# an example of problematic function
def brain_turn():
	logDebug("some message 1")
	try:
		logDebug("some message 2")
		1. / 0. # some code raising an exception
		logDebug("some message 3") # not logged, as it is after error
	except:
		logTraceBack()
'''
######################################################################

# "overwrites" functions in pisqpipe module
pp.brain_init = brain_init
pp.brain_restart = brain_restart
pp.brain_my = brain_my
pp.brain_opponents = brain_opponents
pp.brain_block = brain_block
pp.brain_takeback = brain_takeback
pp.brain_turn = brain_turn
pp.brain_end = brain_end
pp.brain_about = brain_about
if DEBUG_EVAL:
	pp.brain_eval = brain_eval

def main():
	pp.main()

if __name__ == "__main__":
	main()
