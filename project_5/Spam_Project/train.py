#!/usr/bin/env python
"""
This file is used to learn from training set

Anke (Adrian) Li (ankeli@cs.stonybrook.edu)
Stony Brook University
"""
__author__ = 'Adrian'

#from collections import defaultdict
import sys, copy, time, pickle
from guppy import hpy

from my_lib import *

def main():
    if len(sys.argv) != 2:
        print 'Wrong number of arguments:', len(sys.argv)
        print 'Usage: python train.py <train date file name>'
        return
    
    train_fname = sys.argv[1]
    with open(train_fname) as f:
        content = [x.strip('\n') for x in f.readlines()]
    
    #print content[500]
    mails = []
    for line in content:
        elements = line.split(" ")
        
        # check if the number of elements is correct
        if len(elements)%2 != 0:
            print 'Wrong number of elements!'
            return
        
        new_mail = Mail(elements[0], elements[1])
        
        for i in range (2, len(elements), 2):
            new_mail.add_word(elements[i])
        
        mails.append(new_mail)
    
    count_spam = 0
    count_ham = 0
    count_all = len(mails)
    
    dict_spam = dict()
    dict_ham = dict()
    
    for mail in mails:
        #print mail
        
        if mail.type == 'spam':
            count_spam += 1
            for word in mail.words:
                if word in dict_spam:
                    dict_spam[word] += 1
                else:
                    dict_spam[word] = 1
        else:
            count_ham += 1
            for word in mail.words:
                if word in dict_ham:
                    dict_ham[word] += 1
                else:
                    dict_ham[word] = 1
    
    #print dict_spam
    #print dict_ham
    #storing all generated variables into a pickle file
    with open('gen_values.pickle', 'w') as f:
        pickle.dump([count_spam, count_ham, count_all,\
            dict_spam, dict_ham], f)
    
    print 'Finished learning process, exiting...'

main()
