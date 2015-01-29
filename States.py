# -*- coding: utf-8 -*-
"""
Created on Fri Jan 23 13:34:12 2015

@author: olejrogeberg

This file contains the definitions of the State class, along with its
three subclasses NoTreatment, DrugFreeTreatment and OMT.

Currently working on the transfers between states. The top-level State class
has a function for drawing transfers, but I need to transfer the individuals 
who will be shifting states into their correct transfer-sets. Ideally, I would
like to do this in the State class so that I don't need to duplicate this
functionality in each of the three subclasses, but this needs to take into
account that the three different subclasses only ...


"""
import random

class State(object):
    
    def __init__(self):
        self.members=set([])
        self.dead=set([])
        self.od=set([])
        self.transition_omt=set([])
        self.transition_no_treatment=set([])
        self.transition_drug_free_treatment=set([])
        
    def update_members(self):
        for member in self.members:
            member.update(type(self).__name__)
            if member.alive==False:
                self.dead.add(member)
            if member.od==True:
                self.od.add(member)
        for corpse in self.dead:
            self.members.remove(corpse)
            
    def find_transitions(self,year):
        self.transition_omt=set([])
        self.transition_no_treatment=set([])
        self.transition_drug_free_treatment=set([])
        
        for individual in self.members:
            transfer_risks = \
                self.calculate_transfer_risks(individual,year)
            random_draw=random.random()
            if random_draw < transfer_risks["omt"]:
                self.transition_omt.add(individual)
            elif random_draw < (transfer_risks["omt"] + \
                transfer_risks["no_treatment"]):
                self.transition_no_treatment.add(individual)
            else:
                self.transition_drug_free_treatment.add(individual)
                
    def receive_members(self,individuals):
        for individual in individuals:
            self.members.add(individual)
            
    def give_members(self,state_type):
        transfers = set([])
        if state_type == self.own_state:
            pass
        elif state_type == "omt":
            for member in self.transition_omt:
                transfers.add(member)
                self.members.remove(member)
        elif state_type == "no_treatment":
            for member in self.transition_no_treatment:
                transfers.add(member)                
                self.members.remove(member)
        elif state_type == "drug_free_treatment":
            for member in self.transition_drug_free_treatment:
                transfers.add(member)
                self.members.remove(member)
        return transfers
            
            
    def summarize(self):
        """Exports information on the state,
        such as number of members, their age,
        their use level etc"""
        pass
        
class NoTreatment(State):
    use_shock = (0,0)
    use_risk = 0.0
    death_risk_shock = 1

    def __init__(self):
        super(NoTreatment,self).__init__()
        self.own_state="no_treatment"
        
    def update(self):
        super(NoTreatment,self).update_members()
        
    def transfer_risk_drug_free_treatment(self,individual,year):
        return 0.1
    def transfer_risk_omt(self,individual,year):
        """This probability should vary over time, given the change in
        OMT capacity and intake criteria."""
        if year < 10:
            return 0.01
        else:
            return 0.2
            
    def calculate_transfer_risks(self,individual,year):
        risks = {}
        risks["drug_free_treatment"] = \
            self.transfer_risk_drug_free_treatment(individual,year)
        risks["omt"]=self.transfer_risk_omt(individual,year)
        risks["no_treatment"]=(1-risks["omt"]-risks["drug_free_treatment"])
        return risks
        
class DrugFreeTreatment(State):
    use_shock = (-5,2)
    use_risk = -0.1
    death_risk_shock = 0.7

    def __init__(self):
        super(DrugFreeTreatment,self).__init__()
        self.own_state="drug_free_treatment"
        
    def update(self):
        super(DrugFreeTreatment,self).update_members()
        
    def transfer_risk_no_treatment(self,individual,year):
        return 0.3
    def transfer_risk_omt(self,individual,year):
         return 0
        
    def calculate_transfer_risks(self,individual,year):
        risks = {}
        risks["no_treatment"]  = \
            self.transfer_risk_no_treatment(individual,year)
        risks["omt"]=self.transfer_risk_omt(individual,year)
        risks["drug_free_treatment"]=(1-risks["no_treatment"]-risks["omt"])
        return risks

class OMT(State):
    use_shock = (-2,1)
    use_risk = -0.3
    death_risk_shock = 0.7

    def __init__(self):
        super(OMT,self).__init__()
        self.own_state="omt"
        
    def update(self):
        super(OMT,self).update_members()
        
    def transfer_risk_no_treatment(self,individual,year):
        return 0.05
    def transfer_risk_drug_free_treatment(self,individual,year):
        return 0.05
        
    def calculate_transfer_risks(self,individual,year):
        risks = {}
        risks["no_treatment"]= \
            self.transfer_risk_no_treatment(individual,year)
        risks["drug_free_treatment"] = \
            self.transfer_risk_drug_free_treatment(individual,year)
        risks["omt"]=(1-risks["no_treatment"]-risks["drug_free_treatment"])
        return risks
       

        
