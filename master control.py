# -*- coding: utf-8 -*-
"""
This file sources and runs specific simulations.
"""

from user import User
from states import State, NoTreatment, DrugFreeTreatment, OMT
from society import Society
import random

soc = Society(1000)

soc.run_several_years(10)
