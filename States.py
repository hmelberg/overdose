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

NO - Here's how I can do it: Each class returns a probability for each of the
three states - including itself (1- the sum of the two transition
 probabilities). The superclass sorts the members within any class into three
 groups: Those "transitioning" to state 1, 2 or 3 (in other words, including
 stayers). The superclass can have a function for ejecting as well as 
 receiving a set of individuals - and the subclasses can call these as 
 appropriate.
"""


class State(object):
    
    def __init__(self):
        self.members=set([])
        self.dead=set([])
        self.od=set([])
        
    def update_members(self,state):
        for member in self.members:
            member.update(state)
            if member.alive==False:
                self.dead.add(member)
            if member.od==True:
                self.od.add(member)
        for corpse in self.dead:
            self.members.remove(corpse)
            
    def transfer_draw(self,year):
        for individual in self.members:
            transfer_risks = \
                individual.calculate_transfer_risks(individual,year)
            state_list=transfer_risks.keys()
            random_draw=random.random()
            if random_draw < transfer_risks[state_list[0]]:
                new_state=0
            else if random_draw < transfer_risks[state_list[0]]+ \
                transfer_risks[state_list[1]]:
                new_state=1
            else:
                new_state=2 
            
    def summarize(self):
        """Exports information on the state,
        such as number of members, their age,
        their use level etc"""
        pass
        
class NoTreatment(State):
    use_shock = (0,0)
    use_risk_shock = 1
    death_risk_shock = 1

    def __init__(self):
        super(State,self).__init__()
        self.transfers_drug_free_treatment=set([])
        self.transfers_omt=set([])
        
    def update(self):
        super(State,self).update_members("NoTreatment")
        
    def transfer_risk_drug_free_treatment(self,individual,year):
        0.1
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
        return risks
        
class DrugFreeTreatment(State):
    use_shock = (-5,2)
    use_risk = 1
    death_risk_shock = 0.7

    def __init__(self):
        super(State,self).__init__()
        self.transfers_omt=set([])
        self.transfers_no_treatment=set([])
        
    def update(self):
        super(State,self).update_members("DrugFreeTreatment")
        
    def transfer_risk_no_treatment(self,individual,year):
        0.3
    def transfer_risk_omt(self,individual,year):
        0
        
    def calculate_transfer_risks(self,individual,year):
        risks = {}
        risks["no_treatment"] \ =
            self.transfer_risk_no_treatment(individual,year)
        risks["omt"]=self.transfer_risk_omt(individual,year)
        return risks



class OMT(State):
    use_shock = (-2,1)
    use_risk = 0.5
    death_risk_shock = 0.7

    def __init__(self):
        super(State,self).__init__()
        self.transfers_no_treatment=set([])
        self.transfers_drug_free_treatment=set([])
        
    def update(self):
        super(State,self).update_members("OMT")
        
    def transfer_risk_no_treatment(self,individual,year):
        0.05
    def transfer_risk_drug_free_treatment(self,individual,year):
        0.05
        
    def calculate_transfer_risks(self,individual,year):
        risks = {}
        risks["no_treatment"]= \
            self.transfer_risk_no_treatment(individual,year)
        risks["drug_free_treatment"] = \
            self.transfer_risk_drug_free_treatment(individual,year)
        return risks
       

        
