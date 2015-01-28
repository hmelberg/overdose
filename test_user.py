# -*- coding: utf-8 -*-
"""
Creates an instance of the class User (in conftest)
 and queries it to check that it behaves
appropriately.
"""

def test_user_age(valid_user):
    assert valid_user.age == 17

def test_user_use(valid_user):
    assert valid_user.use_set_point == 7
    def repeated_change(state):
        for i in range(10):
            valid_user.use_update(state)
            assert valid_user.use_current >= 0
            assert valid_user.use_current <= 10
    repeated_change("OMT")
    repeated_change("NoTreatment")
    repeated_change("DrugFreeTreatment")

def test_od_update(valid_user):
    valid_user.od_risk_update("OMT")
    omt = valid_user.od_risk
    valid_user.od_risk_update("NoTreatment")
    no_treatment=valid_user.od_risk
    valid_user.od_risk_update("DrugFreeTreatment")
    drug_free_treatment=valid_user.od_risk
    assert omt > 0
    assert omt < 1
    assert no_treatment < 1
    assert no_treatment > 0
    assert drug_free_treatment > 0
    assert drug_free_treatment < 1
    assert drug_free_treatment > omt
    assert no_treatment > drug_free_treatment
    
def test_death_risk(valid_user):
    def repeated_change(state):
        for i in range(30):
            valid_user.death_risk_update(state)
            assert valid_user.death_other_risk >= 0
            assert valid_user.death_other_risk <= 1
            valid_user.age += 1
        valid_user.age = 17
    repeated_change("OMT")
    repeated_change("NoTreatment")
    repeated_change("DrugFreeTreatment")
    valid_user.death_risk_update("OMT")
    omt = valid_user.death_other_risk
    valid_user.death_risk_update("NoTreatment")
    no_treatment=valid_user.death_other_risk
    valid_user.death_risk_update("DrugFreeTreatment")
    drug_free_treatment = valid_user.death_other_risk
    assert no_treatment > drug_free_treatment
    assert drug_free_treatment == omt
    
def test_update(valid_user):
    use_pre=valid_user.use_current
    valid_user.update("NoTreatment")
    assert valid_user.age == 18
    assert valid_user.use_history[-1] == use_pre
    assert valid_user.state_history[-1] == "NoTreatment"
    
    