# -*- coding: utf-8 -*-
'''
This module contains scheduler exceptions
'''

class ScheduleException(Exception):
    '''
    Base exception class
    '''
    def __init__(self, message=''):
        super(ScheduleException, self).__init__(message)
        self.strerror = message

class Overtime(ScheduleException):
    '''
    The schedule has gone over its allotted time
    '''

class Undertime(ScheduleException):
    '''
    The schedule has not yet used its allotted time
    '''
