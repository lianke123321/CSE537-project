#!/usr/bin/env python
"""
This file is used to classify test set

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
        print 'Usage: python train.py <test data file name>'
        return
    
    # load test file
    test_fname = sys.argv[1]
    with open(test_fname) as f:
        content = [x.strip('\n') for x in f.readlines()]
    
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
    
    # load processed data
    with open('gen_values.pickle') as f:
        count_spam, count_ham, count_all, dict_spam,\
            dict_ham, dict_all = pickle.load(f)
    
    p_spam = float(count_spam)/count_all
    p_ham = float(count_ham)/count_all
    
    # catagorize each mail
    for mail in mails:
        p_f_spam = 1.0
        p_f_ham = 1.0
        p_f_all = 1.0
        
        for word in mail.words:
            if word in dict_spam:
                p_f_spam = p_f_spam * (float(dict_spam[word]) / count_spam)
            if word in dict_ham:
                p_f_ham = p_f_ham * (float(dict_ham[word]) / count_ham)
            if word in dict_all:
                p_f_all = p_f_all * (float(dict_all[word]) / count_all)
        
        p_is_spam = p_spam * p_f_spam / p_f_all
        p_is_ham = p_ham * p_f_ham / p_f_all
        
        print p_is_spam, p_is_ham
    
    #print p_spam, p_ham

main()
