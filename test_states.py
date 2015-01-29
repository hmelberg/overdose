# -*- coding: utf-8 -*-
"""
Gets prepopulated states from conftest and checks various aspects of the
state functionality
"""
import scipy

def test_no_treatment_aging(state_notreat):
    notreat=state_notreat
    assert len(notreat.members)==1000
    def age_mean():
        ages = []
        for member in notreat.members:
            ages.append(member.age)
        return scipy.mean(ages)
    agemean_pre = age_mean()
    notreat.update()
    agemean_post = age_mean()
    assert agemean_pre == agemean_post -1

def check_deaths(state):
    """Check that some people (out of 1000) die and some OD"""
    some_state = state
    some_state.update()
    assert len(some_state.dead) != 0
    assert len(some_state.od) != 0
    dead_still_member=0
    for person in some_state.dead:
        if person in some_state.members:
            dead_still_member +=1
    assert dead_still_member == 0
    od_still_member = 0
    for person in some_state.od:
        if person in some_state.members:
            od_still_member += 1
    assert od_still_member == 0

def test_no_treatment_deaths(state_notreat):
    check_deaths(state_notreat)
    
def test_drugfree_deaths(state_drugfree):
    check_deaths(state_drugfree)
    
def test_omt_deaths(state_omt):
    check_deaths(state_omt)
    
def checking_transition(state):
    """Check that some people - out of 1000 - are moved to each state,
    and that the sum of people remains 1000"""    
    some_state = state
    assert len(some_state.transition_omt) == 0
    assert len(some_state.transition_no_treatment) == 0
    assert len(some_state.transition_drug_free_treatment) == 0
    some_state.find_transitions(3)
    if type(some_state).__name__ != "DrugFreeTreatment":
        assert len(some_state.transition_omt) != 0
    else:
        assert len(some_state.transition_omt) == 0
    assert len(some_state.transition_no_treatment) != 0
    assert len(some_state.transition_drug_free_treatment) != 0
    assert len(some_state.transition_drug_free_treatment) + \
        len(some_state.transition_no_treatment) + \
        len(some_state.transition_omt) == 1000
        
def test_transition_no_treatment(state_notreat):
    checking_transition(state_notreat)

def test_transition_omt(state_omt):
    checking_transition(state_omt)

def test_transition_drugfree(state_drugfree):
    checking_transition(state_drugfree)
    
def test_member_receipt(state_notreat,extra_users):
    members_pre = len(state_notreat.members)
    state_notreat.receive_members(extra_users)
    members_post = len(state_notreat.members)
    assert members_post == members_pre + 100
    
def test_member_give(state_notreat):
    some_state = state_notreat
    some_state.find_transitions(3)
    members_pre = len(some_state.members)
    exits_drugfree = len(some_state.transition_drug_free_treatment)
    exits_omt = len(some_state.transition_omt)
    some_state.give_members("no_treatment")
    assert len(some_state.members) == members_pre
    some_state.give_members("omt")
    assert len(some_state.members) == members_pre - exits_omt
    some_state.give_members("drug_free_treatment")
    assert len(some_state.members) == members_pre - exits_omt - exits_drugfree
    
