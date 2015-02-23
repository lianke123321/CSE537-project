#!/usr/bin/python
__author__ = 'Adrian'

from collections import defaultdict
import sys
import copy
from guppy import hpy

size = 7


class Tree(object):
    def __init__(self, data, parent, move, g):
        self.data = data
        self.parent = parent
        self.children = {}
        self.move = move
        self.dead = False
        self.g = g
        self.h = 1000


def init():
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
    # print '\n'
    for i in range(0, size):
        for k in range(0, size):
            sys.stdout.write(str(board[i][k]) + ' ')
        sys.stdout.write('\n')
    print '\n'


def get_next_move(board):
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
    if board[3][3] == 'x':
        for i in range(0, size):
            for k in range(0, size):
                if i != 3 and k != 3:
                    if board[i][k] == 'x':
                        return False
    else:
        return False

    print 'Reached final state!'
    draw_board(board)
    return True


def cut_edge(node):
    count = 0
    for i in range(0, len(node.children)):
        if (len(get_next_move(node.children[i].data)) == 0) and (node.children[i].data[3][3] != 'x'):
            node.children[i].dead = True
            count += 1
    print ('Cut %d edge(s)!' % count)


def iddfs(node, depth):
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
                result, sub_move = iddfs(node.children[i], depth - 1)
                if result:
                    print sub_move
                    return result, node.move
                else:
                    i += 1
            return False, node.move
        else:
            return False, node.move


def heuristic_1(node, opt):
    h = 0
    for i in range(0, size):
        for k in range(0, size):
            if node.data[i][k] != opt[i][k]:
                h += 1
    print 'Heuristic 1 result: ', h
    return h


def heuristic_2(node, opt):
    h = 0
    for i in range(0, size):
        for k in range(0, size):
            if node.data[i][k] == 'x':
                h += (abs(i-3) + abs(k-3))
    print 'Heuristic 2 result: ', h
    return h


def a_star_search(node, opt, depth):
    if check_finish(node.data):
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
                node.children[i].h = heuristic_2(node.children[i], opt)
                draw_board(node.children[i].data)
                print 'Child ' + str(i) + ' initialized!'
                i += 1

            print 'Number of children: ', len(node.children)
            cut_edge(node)

            while True:
                tmp_cost = 100
                chosen = 0
                for i in range(0, len(node.children)):
                    # print ("%d: %d" % (i, node.children[i].h))
                    # print ("Child %d is dead? %r" % (i, node.children[i].dead))
                    if not node.children[i].dead:
                        if node.children[i].h <= tmp_cost:
                            chosen = i
                            tmp_cost = node.children[i].h

                print 'Choosing: child ', chosen
                draw_board(node.children[chosen].data)
                result = a_star_search(node.children[chosen], opt, depth)
                if not result:
                    # print 'Dead end! Number of children before delete: ', len(node.children)
                    # del node.children[chosen]
                    # print 'Dead end! Number of children: ', len(node.children)
                    node.children[chosen].dead = True
                    if len(node.children) == 0:
                        return False
                else:
                    return result

        else:
            node.dead = True
            print 'No next move, return false!'
            return False


def main():
    board, opt = init()
    # draw_board(opt)
    root = Tree(board, None, None, 0)
    depth = 0
    '''
    while True:
        result, move_seq = iddfs(root, depth)
        if result:
            break
        else:
            depth += 1

    print '\nBelow is memory usage for Iterative Deepening Search:\n'
    print hpy().heap()
    '''
    print '\nNow we do A* search using heuristic 1'
    print a_star_search(root, opt, 0)


main()