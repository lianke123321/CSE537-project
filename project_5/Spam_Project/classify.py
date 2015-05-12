#!/usr/bin/env python
"""
This file is used to classify test set

Anke (Adrian) Li (ankeli@cs.stonybrook.edu)
Stony Brook University
"""
__author__ = 'Adrian'

#from collections import defaultdict
import sys, copy, time, pickle, math
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
            new_mail.add_word(elements[i], elements[i+1])
        
        mails.append(new_mail)
    
    # load processed data
    with open('gen_values.pickle') as f:
        count_spam, count_ham, count_all, dict_spam,\
            dict_ham, dict_all = pickle.load(f)
    
    p_spam = float(count_spam)/count_all
    p_ham = float(count_ham)/count_all
    #print p_spam, p_ham
    
    correct_num = 0
    
    # catagorize each mail
    for mail in mails:
        # use logarithm here cause the actual number is too small
        p_f_spam_log = 0
        p_f_ham_log = 0
        # p_f_all is not used since it's the common denominator
        #p_f_all = 1.0
        
        for word in mail.words:
            if word in dict_spam:
            #if (word in dict_spam) and (word in dict_ham):
                #p_fi_spam_log = math.log(float(mail.words[word])/dict_spam[word])
                p_fi_spam_log = math.log(float(dict_spam[word]) / dict_all[word])
                
            else:
                #print 'Word {} is not in dict_spam!'.format(word)
                # apply Laplace smoothing here
                p_fi_spam_log = math.log(float(1) / (count_spam + 2))
            
            p_f_spam_log += p_fi_spam_log
            
            if word in dict_ham:
                #p_fi_ham_log = math.log(float(mail.words[word]) / dict_ham[word])
                p_fi_ham_log = math.log(float(dict_ham[word]) / dict_all[word])
                
            else:
                #print 'Word {} is not in dict_ham!'.format(word)
                # apply Laplace smoothing here
                p_fi_ham_log = math.log(float(1) / (count_ham + 2))
                
            p_f_ham_log += p_fi_ham_log
        
        # whoever is greater, means a larger possibility
        # the mail is spam/ham
        p_is_spam_log = p_spam * p_f_spam_log
        p_is_ham_log = p_ham * p_f_ham_log
        
        result = ''
        if p_is_spam_log >= p_is_ham_log:
            result = 'spam'
        else:
            result = 'ham'
        
        if result == mail.type:
            #print 'Got it', result
            correct_num += 1
    
    p_correct = float(correct_num) / len(mails)
    print 'Correctly identified {} mails. Accuracy: {}'.format(correct_num, p_correct)

main()
