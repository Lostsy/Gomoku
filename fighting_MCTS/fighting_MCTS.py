import random
import gomoku_util as util
import MCTS_util as mcts
import pisqpipe as pp
from pisqpipe import DEBUG_EVAL, DEBUG

pp.infotext = 'name="fighting_random", author="Ding", version="0.0", country="China", www="https://github.com/stranskyjan/pbrain-pyrandom"'
MAX_BOARD = 20
gomoku = util.Gomoku(MAX_BOARD, MAX_BOARD)

def brain_init():
    if pp.width < 5 or pp.height < 5:
        pp.pipeOut("ERROR size of the board")
        return
    if pp.width > MAX_BOARD or pp.height > MAX_BOARD:
        pp.pipeOut("ERROR Maximal board size is {}".format(MAX_BOARD))
        return
    gomoku = util.Gomoku(pp.height, pp.width)
    pp.pipeOut("OK")


def brain_restart():
    gomoku.restart()
    pp.pipeOut("OK")


def brain_my(x, y):
    if gomoku.is_free(x,y):
        gomoku.make_move(x,y,1)
    else:
        pp.pipeOut("ERROR my move [{},{}]".format(x, y))


def brain_opponents(x, y):
    if gomoku.is_free(x,y):
        gomoku.make_move(x,y,2)
    else:
        pp.pipeOut("ERROR opponents's move [{},{}]".format(x, y))


def brain_block(x, y):
    if gomoku.is_free(x,y):
        gomoku.make_move(x,y,3)
    else:
        pp.pipeOut("ERROR winning move [{},{}]".format(x, y))


def brain_takeback(x, y):
    if gomoku.is_occupied(x, y):
        gomoku.take_back(x, y)
        return 0
    return 2


def brain_turn():
    root_mcts_node = mcts.Gomoku_MCTS(gomoku,None)
    gomoku_mcts = mcts.MonteCarloTreeSearch(root_mcts_node)
    best_move = gomoku_mcts.best_action()
    pp.do_mymove(*best_move)
    pass


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
        board = gomoku.get_board()
        c = str(board[x][y])
        win32gui.ExtTextOut(dc, rc[2]-15, 3, 0, None, c, ())
        win32gui.ReleaseDC(wnd, dc)

######################################################################
# A possible way how to debug brains.
# To test it, just "uncomment" it (delete enclosing """)
######################################################################

# # define a file for logging ...
# DEBUG_LOGFILE = "C:\\Users\\zkdin\\Downloads\\piskvork\\tmp\\fighting_random.log"
# # ...and clear it initially
# with open(DEBUG_LOGFILE,"w") as f:
# 	pass

# # define a function for writing messages to the file
# def logDebug(msg):
# 	with open(DEBUG_LOGFILE,"a") as f:
# 		f.write(msg+"\n")
# 		f.flush()

# # define a function to get exception traceback
# def logTraceBack():
# 	import traceback
# 	with open(DEBUG_LOGFILE,"a") as f:
# 		traceback.print_exc(file=f)
# 		f.flush()
# 	raise

# use logDebug wherever
# use try-except (with logTraceBack in except branch) to get exception info
# an example of problematic function
# def brain_turn():
# 	logDebug("some message 1")
# 	try:
# 		logDebug("some message 2")
# 		1. / 0. # some code raising an exception
# 		logDebug("some message 3") # not logged, as it is after error
# 	except:
# 		logTraceBack()

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
