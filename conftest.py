# -*- coding: utf-8 -*-
"""
Created on Wed Jan 28 10:12:54 2015

@author: olejrogeberg
"""

from user import User
from states import State, NoTreatment, DrugFreeTreatment, OMT

def pytest_funcarg__valid_user(request):
    return User(17,7)

""" We next need to create a set of states populated with users, to make it
possible to test the state functionality"""

def pytest_funcarg__state_notreat(request):
    def make_user_set(number):
        users = set([])
        for i in range(number):
            users.add(User(17,5))
        return users
    state = NoTreatment()
    state.receive_members(make_user_set(1000))
    return state
    