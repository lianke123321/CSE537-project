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
    def __init__(self, name, class_time):
        self.name = name
        self.class_time = class_time
        self.ta_num = None
        self.rec_time = None    # recitation time
        self.ta_attend = None
        self.ta_skills = None

    def print_me(self):
        print 'Course name:', self.name, 'class time:', self.class_time, 'ta num:', self.ta_num,\
            'recitation time:', self.rec_time, 'ta_attend?', self.ta_attend, 'skills:', self.ta_skills


class TA(object):
    """
    This class stores ta information
    """
    def __init__(self, name, busy_time):
        self.name = name
        self.busy_time = busy_time
        self.skills = None

    def print_me(self):
        print 'TA name:', self.name, 'busy time:', self.busy_time, 'skills:', self.skills


def parse_file(dataset, course_list, ta_list):
    raw_data = open(dataset)
    tables = raw_data.read().split("\n\n", 6)
    table_course_time = tables[0].split("\n")
    table_course_recitation = tables[1].split("\n")
    table_course_details = tables[2].split("\n")
    table_course_skills = tables[3].split("\n")
    table_ta_busy = tables[4].split("\n")
    table_ta_skills = tables[5].split("\n")
    print 'length: ', len(table_course_time), len(table_course_recitation), len(table_course_details), \
        len(table_course_skills), len(table_ta_busy), len(table_ta_skills)
    # print 'table_course_time: ', table_course_time
    for course in table_course_time:
        items = course.split(",")
        course_name = items[0].strip()
        class_time = []
        i = 1
        while i < len(items):
            class_time.append((items[i].strip(), items[i+1].strip()))
            i += 2

        new_course = Course(course_name, class_time)
        # new_course.print_me()
        course_list.append(new_course)

    for course in table_course_recitation:
        items = course.split(",")
        course_name = items[0].strip()
        rec_time = []
        i = 1
        while i < len(items):
            rec_time.append((items[i].strip(), items[i+1].strip()))
            i += 2
        for course_node in course_list:
            if course_name == course_node.name:
                course_node.rec_time = rec_time

    for course in table_course_details:
        items = course.split(",")
        course_name = items[0].strip()
        student_num = int(items[1].strip())
        require_attendance = False
        if items[2].strip() == 'yes':
            require_attendance = True
        # print 'course name:', course_name, 'student num:', student_num, 'require attendance?', require_attendance
        course_node = next((x for x in course_list if x.name == course_name), None)
        course_node.ta_attend = require_attendance
        if student_num < 40:
            course_node.ta_num = 0.5
        elif student_num < 60:
            course_node.ta_num = 1.5
        else:
            course_node.ta_num = 2.0

    for course in table_course_skills:
        items = course.split(",")
        course_name = items[0].strip()
        course_skills = []
        for i in range(1, len(items)-1):
            course_skills.append(items[i].strip())
        course_node = next((x for x in course_list if x.name == course_name), None)
        course_node.ta_skills = course_skills

    # for course_node in course_list:
    #     course_node.print_me()

    for line in table_ta_busy:
        items = line.split(",")
        ta_name = items[0].strip()
        ta_busy_time = []
        i = 1
        while i < len(items):
            ta_busy_time.append((items[i].strip(), items[i+1].strip()))
            i += 2

        new_ta = TA(ta_name, ta_busy_time)
        ta_list.append(new_ta)

    for line in table_ta_skills:
        items = line.split(",")
        ta_name = items[0].strip()
        ta_skills = []
        for i in range(1, len(items)-1):
            ta_skills.append(items[i].strip())
        ta_node = next((x for x in ta_list if x.name == ta_name), None)
        ta_node.skills = ta_skills

    # for ta_node in ta_list:
    #     ta_node.print_me()


script, filename = sys.argv
course_list = []
ta_list = []

parse_file(filename, course_list, ta_list)
print 'course_list length:', len(course_list), 'ta_list length:', len(ta_list)