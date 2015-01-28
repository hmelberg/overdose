# -*- coding: utf-8 -*-
"""
Created on Fri Jan 23 13:37:08 2015

@author: olejrogeberg

This file contains the class User, which describes an individual user, as well
as providing methods for updating the user's use-level, history, death and OD
risks over time.
"""

import random
import math
from states import State, NoTreatment, DrugFreeTreatment, OMT

class User(object):
    use_mean_reversion=0.2
    use_shock_sd=2

    def __init__(self,age,use_set_point):
        self.age=age
        self.death_other_risk = 0
        self.od_risk = 0
        self.use_set_point=use_set_point
        self.state_history=list("")
        self.use_history=[0]
        self.use_current=0
        self.use_update("NoTreatment")
        self.alive = True
        self.od = False

    def od_risk_update(self,state):
        """Calculates the risk of overdose, which is influenced by the state.
        To ensure that the probability stays between 0 and 1 I have used
        a logit-link function."""
        
        if state == "OMT":
            state_risk = OMT.use_risk
        elif state == "DrugFreeTreatment":
            state_risk = DrugFreeTreatment.use_risk
        elif state == "NoTreatment":
            state_risk = NoTreatment.use_risk
            
        own_use_risk_input = -1 + 0.5 * (self.use_current - 5) + \
            0.1 * (self.use_current - self.use_history[-1]) + state_risk
        own_use_risk = math.exp(own_use_risk_input)/ \
            (1+math.exp(own_use_risk_input))
        self.od_risk = own_use_risk
        
        
    def use_update(self,state):
        random_drift = self.use_current + \
            User.use_mean_reversion * (self.use_set_point - self.use_current) \
            + random.normalvariate(0,User.use_shock_sd)
        if state == "OMT":
            state_shock = OMT.use_shock
        elif state == "DrugFreeTreatment":
            state_shock = DrugFreeTreatment.use_shock
        elif state == "NoTreatment":
            state_shock = NoTreatment.use_shock
        self.use_current = min(10,max(0,random_drift + \
            random.normalvariate(state_shock[0],state_shock[1])))
        
    def death_risk_update(self,state):
        initial_risk = 0.001 * 1.05 ** (self.age-18.0)
        if state == "OMT":
            state_shock = OMT.death_risk_shock
        elif state == "DrugFreeTreatment":
            state_shock = DrugFreeTreatment.death_risk_shock
        elif state == "NoTreatment":
            state_shock = NoTreatment.death_risk_shock
        self.death_other_risk = initial_risk * state_shock

    def risk_draw(self):
        draw = random.random()
        if draw < self.od_risk:
            self.alive = False
            self.od = True
        elif draw < self.od_risk + self.death_other_risk:
            self.alive = False
        
    def update(self,state):
        self.age += 1
        self.use_history.append(self.use_current)
        self.state_history.append(state)
        self.use_update(state)
        self.death_risk_update(state)
        self.od_risk_update(state)
        self.risk_draw()
        
        


