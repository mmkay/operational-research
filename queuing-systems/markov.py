#!/usr/bin/env python

"""markov.py - simulation of markov queuing systems with single buffer 
and separate buffer for each user."""

__author__ 	= "Mateusz 'mmkay' Kulewicz"
__copyright__	= "Copyright 2014, Mateusz Kulewicz"
__license__ = "MIT"

from math import pow

"""M/M/1/Q system parameters"""

"""Mean interval between requests for one user in seconds"""
mean_interval = 6.0
"""Mean length of document in bytes"""
mean_length = 600.0
"""Processor speed in bytes / s """
processor_speed = 24000.0
"""Maximum loss"""
max_loss = 0.001
"""Maximum multiplication of system delay. It means that mean system delay of
a document shall not exceed the multiple of mean_length / processor_speed"""
multiplication_max = 5.0

"""Calculates load for one user"""
def one_user_load():
  return mean_length / (mean_interval * processor_speed)
  
def total_load(users):
  return users * one_user_load()
  
def probability_k_elems_in_queue(users, k, queue):
  r = total_load(users)
  return pow(r,k)*((1-r)/(1 - pow(r, queue+1)))
  
def loss(users, queue):
  return probability_k_elems_in_queue(users, queue, queue)
  
def mean_calls_in_system(users, queue):
  sum = 0.0
  for i in range(0, queue):
    sum += i * probability_k_elems_in_queue(users, i, queue)
  return sum
 
def multiplied_system_delay_multiple_queues(users, buffer):
  return mean_calls_in_system(users, buffer) / (one_user_load() * (1 -  loss(users, buffer)))
  
def multiplied_system_delay_single_queue(users, buffer):
  return multiplied_system_delay_multiple_queues(users, buffer) / users

"""Does the simulation of multiple-queue markov system. Finds out the maximum 
number of users and ideal buffer size for such a load"""
def multiple_queues():
  #start values
  users = 1
  
  at_least_one_success = True
  while(at_least_one_success):
    at_least_one_success = False
    for buf in range(1,100):
      if (loss(users, buf) < max_loss and multiplied_system_delay_multiple_queues(users, buf) < multiplication_max):
        at_least_one_success = True
        print("System fits requirements for " + str(users) + " users and buffer " + str(buf))
        print("Loss " + str(loss(users,buf)) + ", delay_multiple " + str(multiplied_system_delay_multiple_queues(users, buf)))
    users += 1
    
def single_queue():
  users = 1
  at_least_one_success = True

  while(at_least_one_success):
    at_least_one_success = False
    for buf in range(1,100):
      if(loss(users, buf) < max_loss and multiplied_system_delay_single_queue(users, buf) < multiplication_max):
      	at_least_one_success = True
      	print("System fits requirements for " + str(users) + " users and buffer " + str(buf))
      	print("Loss " + str(loss(users, buf)) + ", delay_single " + str(multiplied_system_delay_single_queue(users, buf)))
    users += 1
      
"""Run the program"""
print("Running for multiple queues")
multiple_queues()
print("Running for single queue")
single_queue()  
