# -*- coding: utf-8 -*-
'''
Scheduler
'''

# Import Python libraries
import time
import logging

log = logging.getLogger(__name__)

class Scheduler(object):
    '''
    A scheduler
    '''
    def __init__(self, schedules, tick_rate, min_time, max_time):
        '''
        Create a scheduler instance

        :param list Schedule schedule: The schedules for this schedular to manage
        :param float tick_rate: The tick on which to evaluate the timing
        '''
        self.schedules = schedules
        self.tick_rate = tick_rate
        self.clock = Clock()
    

    @property
    def parents(self):
        '''
        Return the parents of this scheduler
        '''
        #TODO
        pass

    @property
    def children(self):
        '''
        Return the children of this scheduler
        '''
        #TODO
        pass

    def run(self):
        '''
        The main loop for the scheduler

        This continues its thread of execution until either all operations
        have run and min_time has been exceeded or until max_time expires. 
        '''
        try:
            for schedule in self.schedules:
                for ret in schedule.run():
                    log.trace('Operation result: {0}'.format(ret))
                    # Check the clock to see if we are out of time in this schedule
                    self.clock.check_clock()
                # Check the clock between schedules as well
                self.clock.check_clock()
        except Overtime:
            self.transition()

    def transition(self):
        '''
        Pass control to the approrpriate scheduler
        
        This will be a child if one exists, otherwise
        control shall be returned to the parent.
        '''
        # This interfaces with the data store to determine which
        # schedule to continue on with

        # PSEUDOCODE! FIXME
        if self.children:
            for child in self.children:
                child.run()
        else:
            # Return control to parent
            # Not sure how this will work yet
            pass


        
class Clock(object):
    '''
    Class to wrap helpers around Python's clock module
    '''
    def __init__(self, min_time, max_time):
        # The ID of the monotonic clock
        #
        # This clock will not be subject to NTP
        # adjustements or any such nonsense.
        self.clock_id = time.CLOCK_MONOTONIC_RAW
        self.min_time = min_time
        self.max_time = max_time


    def cur_time(self):
        '''
        A wrapper to ensure we always return monotonic time
        '''
        return time.monotonic()

    def check_clock(self, min):
        '''
        Examine the schedule to see if there is remaining time
        in this run

        If we haven't spent enough time in this schedule, sleep here

        If we have exceeded the allotted time for this schedule,
        then raise an Overtime exception
        keep the tick rate on track.
        '''
        cur_time = self.clock.cur_time()



class Schedule(object):
    '''
    Represents a schedule
    '''
    def __init__(self, operations, min_time=None, max_time=None):
        '''
        A schedule contains a list of operations
        :param list operations: A list of functions to execute
        :param float min_time: The minimum time this schedule should take
        :param float max_time: The maximum time this schedule should take

        '''
        self.operations = operations
        self.min_time = min_time
        self.max_time = max_time
        self._last_time = None


    def run(self):
        '''
        Run the schedule!
        '''
        while True:
            for operation in self.schedule.operations:
                yield operation()


class Operation(object):
    '''
    An item to be scheduled

    Each operation should be non-blocking

    :param function func: A function  
    '''
    def __init__(self, func):
        self.func = func


