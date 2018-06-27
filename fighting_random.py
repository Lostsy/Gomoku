import random
import gomoku_util as util
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
    if gomoku.is_free(x, y):
        gomoku.make_move(x, y, 1)
    else:
        pp.pipeOut("ERROR my move [{},{}]".format(x, y))


def brain_opponents(x, y):
    if gomoku.is_free(x, y):
        gomoku.make_move(x, y, 2)
    else:
        pp.pipeOut("ERROR opponents's move [{},{}]".format(x, y))


def brain_block(x, y):
    if gomoku.is_free(x, y):
        gomoku.make_move(x, y, 3)
    else:
        pp.pipeOut("ERROR winning move [{},{}]".format(x, y))


def brain_takeback(x, y):
    if gomoku.is_occupied(x, y):
        gomoku.take_back(x, y)
        return 0
    return 2


def brain_turn():
    if pp.terminateAI:
        return
    i = 0
    while True:
        x = random.randint(0, pp.width - 1)
        y = random.randint(0, pp.height - 1)
        i += 1
        if pp.terminateAI:
            return
        if gomoku.is_free(x, y):
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
        board = gomoku.get_board()
        c = str(board[x][y])
        win32gui.ExtTextOut(dc, rc[2] - 15, 3, 0, None, c, ())
        win32gui.ReleaseDC(wnd, dc)


def GA(gomoku):
    CHECK_SCOPE = 2  # the range para
    PATTERN_REWARD = [1023, 511, 255, 127, 63, 31, 15, 7, 3, 1, 0]

    def round_check(board, x, y, scope):
        # given a position (x,y) and scope(integer), check the positions around and return a position list that can make a move.
        position = []
        for i in range(max(0, x - scope), min(x + scope + 1, MAX_BOARD)):
            for j in range(max(0, y - scope), min(y + scope + 1, MAX_BOARD)):
                if board[i][j] == 0:
                    position.append((i, j))
        return

    def position2check(board):
        p2c = []
        board = gomoku.state[0]
        for i in range(MAX_BOARD):
            for j in range(MAX_BOARD):
                if board[i][j] != 0:
                    rounds = round_check(board, i, j, CHECK_SCOPE)
                    for item in rounds:
                        if item not in p2c:
                            p2c.append(item)
        return p2c

    def create_lines(gomoku, x, y):
        # check x l
        x_l = ""
        for i in range(x - 1,max(0,x-5)-1,-1):
            x_l += str(gomoku[i][y])
        # check x r
        x_r = ""
        for i in range(x + 1, min(MAX_BOARD, x + 6)):
            x_r += str(gomoku[i][y])
        # check y up
        y_up = ""
        for i in range(y + 1, min(MAX_BOARD, y + 6)):
            y_up += str(gomoku[x][i])
        # check y down
        y_down = ""
        for i in range(y - 1, max(0, y - 5)-1, -1):
            y_down += str(gomoku[x][i])
        # check \up
        l2bup = ""
        for i in range(x - 1, max(0, x - 5)-1, -1):
            l2bup += str(gomoku[i][y + (x - i)])
        # check \down
        l2bdown = ""
        for i in range(x + 1, min(MAX_BOARD, x + 6)):
            l2bdown += str(gomoku[i][y + (x - i)])
        # check /up
        r2tup = ""
        for i in range(y + 1, min(MAX_BOARD, y + 6)):
            r2tup += str(gomoku[x - y + i][i])
        # check /down
        r2tdown = ""
        for i in range(y - 1, max(0, y - 5) - 1):
            r2tdown += str(gomoku[x - y + i][i])
        return [[x_l, x_r], [y_up, y_down], [l2bup, l2bdown], [r2tup, r2tdown]]

    def createline(board, x, y):
        x_axis = "".join([str(board[x][i]) for i in range(MAX_BOARD)])
        y_axis = "".join([str(board[i][y]) for i in range(MAX_BOARD)])
        backslash = "".join([str(board[x+i][y-i]) for i in range(max(-x, MAX_BOARD + y), min(MAX_BOARD - x, y))])
        slash = "".join([str(board[x+i][y+i]) for i in range(max(-x,-y), min(MAX_BOARD - x, MAX_BOARD - y))])
        return [x_axis, y_axis, backslash, slash]

    def pattern_matching(board, x, y, player):
        #12 patterns to recognize
        board[x][y] = player
        lines = createline()
        for item in lines:#Reward 1023
            #活5
            if item.find(str(player)*5) != -1:
                return PATTERN_REWARD[0]
        for item in lines:#Reward 511
            #活4
            if item.find("0" + str(player) * 4 + "0") != -1:
                return PATTERN_REWARD[1]
            #死4+活3
            if (item.find("0"+str(player)*4+"1") != -1 or item.find("1"+str(player)*4+"0") != -1):
                rest = lines.remove(item)
                for item2 in rest:
                    if item2.find("0"+str(player)*3+"0") != -1:
                        return PATTERN_REWARD[1]
            #死4+死4
            if (item.find("0"+str(player)*4+"1") != -1 or item.find("1"+str(player)*4+"0") != -1):
                rest = lines.remove(item)
                for item2 in rest:
                    if (item2.find("0" + str(player) * 4 + "1") != -1 or item2.find("1" + str(player) * 4 + "0") != -1):
                        return PATTERN_REWARD[1]
        for item in lines:#Reward 255
            # 活3+活3
            if item.find("0" + str(player) * 3 + "0") != -1:
                rest = lines.remove(item)
                for item2 in rest:
                    if item2.find("0" + str(player) * 3 + "0") != -1:
                        return PATTERN_REWARD[2]
        for item in lines:#Reward 127
            #死3+活3
            if item.find("0" + str(player) * 3 + "0") != -1:
                rest = lines.remove(item)
                for item2 in rest:
                    if (item2.find("0" + str(player) * 3 + "1") != -1 or item2.find("1" + str(player) * 3 + "0") != -1):
                        return PATTERN_REWARD[3]
        for item in lines:#Reward 63
            #活3
            if item.find("0" + str(player) * 3 + "0") != -1:
                return PATTERN_REWARD[4]
        for item in lines:#Reward 31
            #死4
            if (item.find("0" + str(player) * 4 + "1") != -1 or item.find("1" + str(player) * 4 + "0") != -1):
                return PATTERN_REWARD[5]
        for item in lines:#Reward 15
            #活2+活2
            if item.find("0" + str(player) * 2 + "0") != -1:
                rest = lines.remove(item)
                for item2 in rest:
                    if item2.find("0" + str(player) * 2 + "0") != -1:
                        return PATTERN_REWARD[6]
        for item in lines:#Reward 7
            #死3
            if (item.find("0" + str(player) * 3 + "1") != -1 or item.find("1" + str(player) * 3 + "0") != -1):
                return PATTERN_REWARD[7]
        for item in lines:#Reward 3
            #活2
            if item.find("0"+str(player)*2+"0") != -1:
                return PATTERN_REWARD[8]
        for item in lines:#Reward 1
            # 死2
            if (item.find("0" + str(player) * 2 + "1") != -1 or item.find("1" + str(player) * 2 + "0") != -1):
                return PATTERN_REWARD[9]
        return PATTERN_REWARD[10]






    def fitness_function(para):
        # the function to compute a position's fitness value
        pass

    def cross_fertilize(para):
        # the cross_fertilize function to create new gomoku chains
        pass

    def mutation(para):
        # the mutation to create mutation of gomoku chains with a motation rate
        pass

    def selectionofgod_the_programmer(para):
        # given chains and theri fitness values, make a simulation of natural selection, return a list of new selected gomoku chains
        pass


######################################################################
# A possible way how to debug brains.
# To test it, just "uncomment" it (delete enclosing """)
######################################################################

# # define a file for logging ...
# DEBUG_LOGFILE = "C:\\Users\\zkdin\\Downloads\\piskvork\\tmp\\fighting_random.log"
# # ...and clear it initially
# with open(DEBUG_LOGFILE,"w") as f:
#     pass

# # define a function for writing messages to the file
# def logDebug(msg):
#     with open(DEBUG_LOGFILE,"a") as f:
#         f.write(msg+"\n")
#         f.flush()

# # define a function to get exception traceback
# def logTraceBack():
#     import traceback
#     with open(DEBUG_LOGFILE,"a") as f:
#         traceback.print_exc(file=f)
#         f.flush()
#     raise

# use logDebug wherever
# use try-except (with logTraceBack in except branch) to get exception info
# an example of problematic function
# def brain_turn():
#     logDebug("some message 1")
#     try:
#         logDebug("some message 2")
#         1. / 0. # some code raising an exception
#         logDebug("some message 3") # not logged, as it is after error
#     except:
#         logTraceBack()

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
