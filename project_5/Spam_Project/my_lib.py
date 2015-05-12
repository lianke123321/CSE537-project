#!/usr/bin/env python
"""
This file is used to learn from training set

Anke (Adrian) Li (ankeli@cs.stonybrook.edu)
Stony Brook University
"""
__author__ = 'Adrian'

class Mail(object):
    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.words = []
    
    def add_word(self, word):
        self.words.append(word)
    
    """
    def print_me(self):
        print 'My id is:', self.id
        print 'My type is:', self.type
        print 'I have words: ', self.words
    """
    
    def __str__(self):
        return 'My id is: {}\nMy type is: {}\nI have words: {}'.format(self.id, self.type, self.words)