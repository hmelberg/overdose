# -*- coding: utf-8 -*-
"""
Created on Fri Jan 23 13:40:04 2015

@author: olejrogeberg

This file contains the Society class. An actual simulation will (in the end) be
specified and managed at this level. An instance of this class will contain
one instance of each State sub-class (NoTreatment, DrugFreeTreatment and OMT), 
and a set of methods for updating these, logging, summarizing and 
visualizing events.
"""

from states import State, DrugFreeTreatment, OMT, NoTreatment
from user import User
import random

class Society(object):
    def __init__(self,users):
        self.states = set([])
        self.states.add(NoTreatment())
        self.states.add(DrugFreeTreatment())
        self.states.add(OMT())
        self.year = 0
        self.recruitment(users)
        
    def make_new_user(self,age,use_set_point):
        """ Creates one new user with the specified age and use_set_point,
        with a use and state history list with one entry (0 and "user" 
        respectively, since no one has been in treatment before becoming
        a user)"""
        return User(age,use_set_point)

    def make_more_users(self,inflow):
        new_users = set([])
        for i in range(inflow):
            new_users.add(self.make_new_user(17,10 * random.random()))
        return new_users
        
    def prepare_transitions(self):
        for state in self.states:
            state.find_transitions(self.year)
        
    
    def execute_transitions(self):
        for receiving_state in self.states:
            for giving_state in self.states:
                receiving_state.receive_members(\
                    giving_state.give_members(receiving_state.own_state))
                    
    def state_clean_up(self):
        dead=0
        od=0
        for state in self.states:
            dead += len(state.dead)
            od += len(state.od)
            state.dead = set([])
            state.od = set([])
        print "Dead: " + str(dead) + " OD: " + str(od)
            
    def update_users(self):
        for state in self.states:
            state.update_members()
    
    def run_one_year(self):
        self.year += 1
        self.recruitment(100)
        self.update_users()
        self.state_clean_up()
        self.prepare_transitions()
        self.execute_transitions()
        
    def run_several_years(self,years):
        for i in range(years):
            self.run_one_year()
                
        
    def recruitment(self, users):
        for state in self.states:
            if state.own_state == "no_treatment":
                state.receive_members(self.make_more_users(users))
