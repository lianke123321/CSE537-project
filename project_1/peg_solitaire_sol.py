#!/usr/bin/python
"""
Anke (Adrian) Li (ankeli@cs.stonybrook.edu)
Stony Brook University
"""
__author__ = 'Adrian'

from collections import defaultdict
import sys
import copy
import time
from guppy import hpy

size = 7    # this is the size of game board


class Tree(object):
    """
    This class defined node in the tree
    """
    def __init__(self, data, parent, move, g):
        self.data = data
        self.parent = parent
        self.children = {}
        self.move = move
        self.dead = False   # this label is used to mark this node is dead
        self.g = g
        self.h = 1000   # initialize h to be a large integer


def init():
    """
    This function is used to initialize game board configuration
    and goal state.
    :return: initialized board and final board
    """
    l = lambda: defaultdict(l)
    board = l()
    opt = l()
    for i in range(0, size):
        for k in range(0, size):
            if (0 <= i <= 1 or 5 <= i <= 6) and (0 <= k <= 1 or 5 <= k <= 6):
                board[i][k] = '-'
                opt[i][k] = '-'
            else:
                # board[i][k] = 'x'
                board[i][k] = '0'
                opt[i][k] = '0'

    board[1][3] = board[2][2] = board[2][3] = board[2][4] = board[3][3] = board[4][3] = 'x'
    # board[3][3] = '0'
    opt[3][3] = 'x'
    print 'Initial board configuration:'
    draw_board(board)

    return board, opt


def draw_board(board):
    """
    Draw current board.
    :param board:
    :return: null
    """
    for i in range(0, size):
        for k in range(0, size):
            sys.stdout.write(str(board[i][k]) + ' ')
        sys.stdout.write('\n')
    print '\n'


def get_next_move(board):
    """
    Generate and return all possible next moves
    :param board:
    :return: list of all possible next moves
    """
    # print 'Calculating next move!'
    next_move = []
    for i in range(0, size):
        for k in range(0, size):
            if board[i][k] == 'x':
                if (board[i - 1][k] == 'x') and (board[i - 2][k] == '0'):
                    next_move.append([(i, k), (i - 2, k)])
                if (board[i + 1][k] == 'x') and (board[i + 2][k] == '0'):
                    next_move.append([(i, k), (i + 2, k)])
                if (board[i][k - 1] == 'x') and (board[i][k - 2] == '0'):
                    next_move.append([(i, k), (i, k - 2)])
                if (board[i][k + 1] == 'x') and (board[i][k + 2] == '0'):
                    next_move.append([(i, k), (i, k + 2)])

    # print next_move
    return next_move


def check_finish(board):
    """
    Check if current state is final state. Return true or false
    :param board:
    :return: true or false
    """
    if board[3][3] == 'x':
        for i in range(0, size):
            for k in range(0, size):
                if i != 3 and k != 3:
                    if board[i][k] == 'x':
                        return False
    else:
        return False

    # print 'Reached final state!'
    # draw_board(board)
    return True


def cut_edge(node):
    """
    Prune edges by labeling all nodes with no next move as dead
    :param node:
    :return: null
    """
    count = 0
    for i in range(0, len(node.children)):
        if (len(get_next_move(node.children[i].data)) == 0) and (not check_finish(node.children[i].data)):
            node.children[i].dead = True
            count += 1
    # print ('Cut %d edge(s)!' % count)


def iddfs(node, depth, expanded_nodes):
    """
    Iterative Deepening Search algorithm. Iteratively search each level.
    No edge cutting here.
    :param node:
    :param depth:
    :param expanded_nodes:
    :return: true or false
    """
    expanded_nodes.append(node)     # add new node to expanded nodes list
    if depth == 0:
        if check_finish(node.data):
            return True, node.move
        else:
            return False, node.move
    else:
        next_move = get_next_move(node.data)
        if len(next_move) > 0:
            i = 0
            for move in next_move:
                node.children[i] = Tree(copy.deepcopy(node.data), node, move, 0)
                node.children[i].data[move[0][0]][move[0][1]] = '0'
                node.children[i].data[move[1][0]][move[1][1]] = 'x'
                node.children[i].data[(move[0][0] + move[1][0]) / 2][(move[0][1] + move[1][1]) / 2] = '0'
                # draw_board(node.children[i].data)
                result, sub_move = iddfs(node.children[i], depth - 1, expanded_nodes)
                if result:
                    print sub_move
                    return result, node.move
                else:
                    i += 1
            return False, node.move
        else:
            return False, node.move


'''
def heuristic_1(node, opt):
    h = 0
    for i in range(0, size):
        for k in range(0, size):
            if node.data[i][k] != opt[i][k]:
                h += 1
    # print 'Heuristic 1 result: ', h
    return h
'''


def heuristic_1(node, opt):
    """
    Define h by the number of next moves. Prefer node with
    more number of next moves
    :param node:
    :param opt:
    :return: calculated h value
    """
    h = 100 - len(get_next_move(node.data))
    return h


def heuristic_2(node, opt):
    """
    Define h by the sum of distances from each peg to the center.
    Prefer node with smaller distance.
    :param node:
    :param opt:
    :return: calculated h value
    """
    h = 0
    for i in range(0, size):
        for k in range(0, size):
            if node.data[i][k] == 'x':
                h += (abs(i-3) + abs(k-3))
    # print 'Heuristic 2 result: ', h
    return h


def heuristic_3(node, opt):
    """
    This optional heuristic combined the other two. This could solve
    normal peg solitaire (much more difficult than this homework)
    :param node:
    :param opt:
    :return: calculated h balue
    """
    h = heuristic_1(node, opt) + heuristic_2(node, opt)
    return h


def a_star_search(heuristic, node, opt, depth, expanded_nodes):
    """
    This is A* search algorithm. Make use of cut_edge function.
    :param heuristic:
    :param node:
    :param opt:
    :param depth:
    :param expanded_nodes:
    :return: true or false
    """
    expanded_nodes.append(node)
    if check_finish(node.data):
        print node.move
        return True
    else:
        next_move = get_next_move(node.data)
        if len(next_move) > 0:
            i = 0
            depth += 1  # Initialize g value for all children
            for move in next_move:
                node.children[i] = Tree(copy.deepcopy(node.data), node, move, depth)
                node.children[i].data[move[0][0]][move[0][1]] = '0'
                node.children[i].data[move[1][0]][move[1][1]] = 'x'
                node.children[i].data[(move[0][0] + move[1][0]) / 2][(move[0][1] + move[1][1]) / 2] = '0'
                # node.children[i].h = heuristic_0(node.children[i], opt) + heuristic_2(node.children[i], opt)
                node.children[i].h = heuristic(node.children[i], opt)
                # draw_board(node.children[i].data)
                # print 'Child ' + str(i) + ' initialized!'
                i += 1

            # print 'Number of children: ', len(node.children)
            cut_edge(node)

            while True:
                tmp_cost = 1000
                chosen = 0
                has_valid_child = False
                for i in range(0, len(node.children)):
                    # print ("%d: %d" % (i, node.children[i].h))
                    # print ("Child %d is dead? %r" % (i, node.children[i].dead))
                    if not node.children[i].dead:
                        has_valid_child = True
                        if node.children[i].h <= tmp_cost:     # here only use h value since g values are always the same
                            chosen = i
                            tmp_cost = node.children[i].h
                if has_valid_child:
                    # print 'Choosing: child ', chosen
                    # draw_board(node.children[chosen].data)
                    result = a_star_search(heuristic, node.children[chosen], opt, depth, expanded_nodes)
                    if not result:
                        # print 'Dead end! Number of children before delete: ', len(node.children)
                        # del node.children[chosen]
                        # print 'Dead end! Number of children: ', len(node.children)
                        node.children[chosen].dead = True
                        if len(node.children) == 0:
                            return False
                    else:
                        print node.move
                        return result
                else:
                    return False

        else:
            node.dead = True
            # print 'No next move, return false!'
            return False


def main():
    while True:
        choose_algo = raw_input("Please input which algorithm you want to run\n"
                                "0: IDDFS,\n"
                                "1: A* w/ heuristic 1,\n"
                                "2: A* with heuristic 2,\n"
                                "3: A* with combined heuristics\n"
                                "Your choice: ")
        try:
            choose_algo = int(choose_algo)
            if 0 <= choose_algo <= 3:
                break
            else:
                print "Input exceeds limit! Please type between 0-2."
        except ValueError:
            print 'Input is not an integer!'

    board, opt = init()
    # draw_board(opt)
    root = Tree(board, None, 'origin', 0)
    depth = 0
    expanded_nodes = []   # this is the list of expanded nodes

    if choose_algo == 0:
        print 'Now we do Iterative deepening Search:'
        start_time = time.time()
        while True:
            result, move_seq = iddfs(root, depth, expanded_nodes)
            if result:
                break
            else:
                depth += 1

        print 'Number of expanded nodes: ', len(expanded_nodes)
        print 'Running time for Iterative Deepening Search: ', time.time() - start_time
        print '\nBelow is memory usage for Iterative Deepening Search:\n'
        print hpy().heap()

    elif choose_algo == 1:
        print '\nNow we do A* search using heuristic 1'
        start_time = time.time()
        print a_star_search(heuristic_1, root, opt, 0, expanded_nodes)

        print 'Number of expanded nodes: ', len(expanded_nodes)
        print 'Running time for A* search w/ heuristic 1', time.time() - start_time
        print '\nBelow is memory usage for A* Search using heuristic 1:\n'
        print hpy().heap()

    elif choose_algo == 2:
        print '\nNow we do A* search using heuristic 2'
        start_time = time.time()
        print a_star_search(heuristic_2, root, opt, 0, expanded_nodes)

        print 'Number of expanded nodes: ', len(expanded_nodes)
        print 'Running time for A* search w/ heuristic 2: ', time.time() - start_time
        print '\nBelow is memory usage for A* Search using heuristic 2:\n'
        print hpy().heap()

    elif choose_algo == 3:
        print '\nNow we do A* search using combined heuristics'
        start_time = time.time()
        print a_star_search(heuristic_3, root, opt, 0, expanded_nodes)

        print 'Number of expanded nodes: ', len(expanded_nodes)
        print 'Running time for A* search w/ combined heuristics', time.time() - start_time
        print '\nBelow is memory usage for A* Search using combined heuristics:\n'
        print hpy().heap()

    else:
        print 'Input value error!'

main()