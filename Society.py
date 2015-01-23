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

from States import State, DrugFreeTreatment, OMT, NoTreatment
from User import User
import random

class Society(object):
    def __init__(self):
        self.no_treatment= NoTreatment()
        self.drug_free_treatment= DrugFreeTreatment()
        self.omt = OMT()
        self.year = 0
        
    def make_new_user(self,age,use_set_point):
        """ Creates one new user with the specified age and use_set_point,
        with a use and state history list with one entry (0 and "user" 
        respectively, since no one has been in treatment before becoming
        a user)"""
        self.no_treatment.members.add(User(age,use_set_point)
        
    def add_multiple_users(self, inflow):
        """Adds new users aged 17 to the simulation, with a use_set_point
        randomly drawn between 1 and 10"""
        for i in range(inflow-1):
            self.make_new_user(17,10*random.random())
    
    def 