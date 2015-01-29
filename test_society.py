# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 12:13:58 2015

@author: olejrogeberg
"""

from society import Society
from states import State, NoTreatment, DrugFreeTreatment, OMT
from user import User

def test_society_initialization():
    soc = Society(1000)
    assert len(soc.states) == 3
    for state in soc.states:
        if type(state).__name__ == "NoTreatment":
            assert len(state.members) == 1000
        else:
            assert len(state.members) == 0
    assert soc.year == 0
    
def state_logger(society):
    transitions = {}
    for state in society.states:
        if type(state).__name__ == "NoTreatment":
            transitions["notreat_omt"] = len(state.transition_omt)
            transitions["notreat_drugfree"] = len(state.transition_drug_free_treatment)
        elif type(state).__name__ == "DrugFreeTreatment":
            transitions["drugfree_notreat"] = len(state.transition_no_treatment)
            transitions["drugfree_omt"] = len(state.transition_omt)
        elif type(state).__name__ == "OMT":
            transitions["omt_notreat"] = len(state.transition_no_treatment)
            transitions["omt_drugfree"] = len(state.transition_drug_free_treatment)
    return transitions
    
    
def test_execute_transitions():
    soc = Society(1000)
    soc.prepare_transitions()
    pre_log = state_logger(soc)
    assert pre_log["drugfree_notreat"] == 0
    assert pre_log["drugfree_omt"] == 0
    assert pre_log["omt_notreat"] == 0
    assert pre_log["omt_drugfree"] == 0
    soc.execute_transitions()
    post_n = {}
    for state in soc.states:
        post_n[type(state).__name__]=len(state.members)
    assert post_n["NoTreatment"] == 1000 - pre_log["notreat_omt"] - pre_log["notreat_drugfree"]
    assert post_n["DrugFreeTreatment"] == pre_log["notreat_drugfree"]
    assert post_n["OMT"] == pre_log["notreat_omt"]


def test_update_users():
    soc = Society(1000)
    soc.prepare_transitions()
    soc.execute_transitions()
    soc.update_users()
    dead_pre = 0
    for state in soc.states:
        dead_pre += len(state.dead)
    assert dead_pre != 0
    soc.state_clean_up()
    dead_post = 0
    soc_n = 0
    for state in soc.states:
        dead_post += len(state.dead)
        soc_n += len(state.members)
    assert dead_post == 0
    assert soc_n == 1000 - dead_pre
    
    
    