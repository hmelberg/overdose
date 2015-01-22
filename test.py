Gjenstår:
    
    Skrive overgangsgreier som flytter folk fra en til en annen state
    Skrive nybruker-funksjon som kan brukes til å:
        initialisere en brukerpopoulasjon
        gi nye brukere over tid
    skrive "ettårs" funksjon som:
        oppdaterer medlemmene
        rensker ut døde
        skriver ut logget info
        flytter brukere mellom states
        tar inn nye brukere

import random

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
        
    def update(self):
        super(State,self).update_members("NoTreatment")
        
class DrugFreeTreatment(State):
    use_shock = (-5,2)
    use_risk = 1
    death_risk_shock = 0.7

    def __init__(self):
        super(State,self).__init__()
        
    def update(self):
        super(State,self).update_members("DrugFreeTreatment")


class OMT(State):
    use_shock = (-2,1)
    use_risk = 0.5
    death_risk_shock = 0.7

    def __init__(self):
        super(State,self).__init__()
        
    def update(self):
        super(State,self).update_members("OMT")

        
class User(object):
    use_mean_reversion=0.2
    use_shock_sd=2

    def __init__(self,age,use_set_point):
        self.age=age
        self.death_other_risk = 0
        self.od_risk = 0
        self.use_set_point=use_set_point
        self.state_history=list()
        self.use_history=list()
        self.use_current=use_set_point
        self.alive = True
        self.od = False
    def od_risk_update(self,state):
        own_use_risk = 0.2 * (self.use_current/10.0) * (self.use_current/self.use_history[-1])
        if state == "OMT":
            state_risk = OMT.use_risk
        elif state == "DrugFreeTreatment":
            state_risk = DrugFreeTreatment.use_risk
        elif state == "NoTreatment":
            state_risk = NoTreatment.use_risk
        self.od_risk = own_use_risk * state_risk
        
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
        self.use_current = min(10,max(0,random_drift + state_shock))
    def death_risk_update(self,state):
        initial_risk = 0.001 * 1.02^(self.age-18)
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
        self.use_update(state)
        self.death_risk_update(state)
        self.od_risk_update(state)
        self.risk_draw()
        
        
        