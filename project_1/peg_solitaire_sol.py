#!/usr/bin/python
__author__ = 'Adrian'

from collections import defaultdict
import sys
import copy
from guppy import hpy

size = 7


class Tree(object):
    def __init__(self, data, parent, move):
        self.data = data
        self.parent = parent
        self.children = {}
        self.move = move
        self.dead = False


def init():
    l = lambda: defaultdict(l)
    board = l()
    for i in range(0, size):
        for k in range(0, size):
            if (0 <= i <= 1 or 5 <= i <= 6) and (0 <= k <= 1 or 5 <= k <= 6):
                board[i][k] = '-'
            else:
                board[i][k] = '0'

    board[1][3] = board[2][2] = board[2][3] = board[2][4] = board[3][3] = board[4][3] = 'x'
    #board[3][3] = '0'
    print 'Initial board configuration:'
    draw_board(board)

    return board


def draw_board(board):
    #print '\n'
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

    #print next_move
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
                node.children[i] = Tree(copy.deepcopy(node.data), node, move)
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


def main():
    board = init()
    root = Tree(board, None, None)
    depth = 0

    while True:
        result, move_seq = iddfs(root, depth)
        if result:
            break
        else:
            depth += 1

    print '\nBelow is memory usage for Iterative Deepening Search:\n'
    print hpy().heap()


main()