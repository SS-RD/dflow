# -*- coding: utf-8 -*-
'''
Test the dflow scheduler
'''
# Import python libraries
import random

# Import dflow libraries
import dflow.scheduler.core

funcs = []  # A list of functions to do "work"
scheds = [] # A list of schedules for a scheduler to use

# Scheduler settings
tick_rate = 0.01
min_time=0.005
max_time=0.1

def prep_funcs():
    for i in range(0, 9):
        # Create a func with a random execution time
        funcs.append(rand_sleep_func)  # Func ref


def rand_sleep_func():
    '''
    Create a function with a random sleep time
    '''
    # Return a number between 0 and 1
    sleep_time = random.random()
    time.sleep(sleep_time)


# Create a set of schedules
for i in range(0, 9):
    sched = schedule.core.Schedule(prep_funcs())
    scheds.append(sched)

scheduler = dflow.scheduler.core.Scheuler(scheds, tick_rate, min_time, max_time)

# Do it!
scheduler.run()
