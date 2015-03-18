#!/usr/bin/python
"""
Anke (Adrian) Li (ankeli@cs.stonybrook.edu)
Stony Brook University
"""
import sys


class Course(object):
    """
    This class stores course information
    """
    def __init__(self, name, ta_num, time, ta_attend, ta_skills):
        self.name = name
        self.ta_num = ta_num
        self.time = time
        self.ta_attend = ta_attend
        self.ta_skills = ta_skills


class TA(object):
    """
    This class stores ta information
    """
    def __init__(self, name, busy_time, skills):
        self.name = name
        self.busy_time = busy_time
        self.skills = skills


def parse_file(dataset):
    raw_data = open(dataset)
    tables = raw_data.read().split("\n\n", 6)
    table_course_time = tables[0].split("\n")
    table_course_recitation = tables[1].split("\n")
    table_course_details = tables[2].split("\n")
    table_course_skills = tables[3].split("\n")
    table_ta_busy = tables[4].split("\n")
    table_ta_skills = tables[5].split("\n")
    # print 'length: ', len(table_course_time), len(table_course_recitation), len(table_course_details), \
    #     len(table_course_skills), len(table_ta_busy), len(table_ta_skills)


script, filename = sys.argv

parse_file(filename)