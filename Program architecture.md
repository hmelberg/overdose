Overdose simulation - program architecture
==========================================

# Introduction

In the late nineties the number of injecting addicts in Norway was estimated to be somewhere around 11 000 (xx ref). While some of these injected substances other than opiates (e.g., amphetamines), the number of heroin users was estimated to be in the same vicinity.

Around the turn of the century, opiate maintenance treatment (OMT) programs were gradually phased in. The number of patients given OMT increased rapidly, eventually enrolling more than 7 000 patients (xx ref). While OMT has been found, in Norwegian as well as other data, to substantially reduce the risk of overdose deaths (e.g., with around 50%) - the total number of overdose deaths in Norway remained high and showed little change.

This project aims to develop a micro-simulation that can be used to explore different ways in which this outcome could be explained.

# Hypotheses to be explored

Logically, the explanations must be found in, or be a mix of, a limited set of possibilities. These possibilities also serve to indicate the kind of mechanisms and possibilities that the simulation needs to be able to handle:

1. *Increasing population of users.* If a large number of users has been shifted into a state (OMT) where their overdose risk is lower, then this will have reduced the average overdose risk per user. However, if the total number of users has increased correspondingly, then the same number of users would overdose. E.g., if average risks for 1000 addicts is halved from 0.2 to 0.1, but the number of addicts doubles, then the total number of overdose deaths would remain constant since 0.2 x 1000 = 0.1 x 2000
1. *Increasing overdose risks in non-OMT states.* Consider a situation where the total number of users is constant and a substantial share of them is moved into a lower-risk state (e.g., OMT). The total number of overdose deaths would then remain unchanged if there was a corresponding increase in the risks faced by users in another state. There are two types of risk changes we need to consider:
  1. **Exogenous increase in risk.** This is a risk increase that is due to something  affecting the system from "the outside." E.g.:
    * A *new substance* that increases the overdose risk of users could be introduced into drug markets or become cheaper/more available.
    * A *shift in police strategy* could push users to use in more risky ways, for instance if a raised risk of being "caught" makes users consume their drugs more quickly, more often alone, and in locations where others are less likely to observe overdoses and respond appropriately.
    * *New users* may have different characteristics and higher or more risky use levels or patterns.
  1. **Endogenous increase in risk.** These are changes that are caused by other changes taking place within the system we are modelling. E.g.:
      * **Interactions between states:** E.g.:
        * *Drug leakage from OMT* may increase as the number of patients on OMT increases, affecting the use risks of those who remain outside of treatment.
        * *Users exiting treatment* may have a temporarily heightened risk of overdose. If the system has a lot of "churn" with users shifting often between states, this could raise the average risk faced by those outside of treatment.
        * *Fewer experienced users outside of treatment* could reduce the transfer of experience and informal guidelines and use-culture to new users.
        * *Fewer users outside of treatment.* If users entering treatment tend to reduce their social contact with users remaining outside of the treatment system, then a declining number of users outside of treatment could make them more likely to use alone or with fewer people around them. This could make an accidental overdose less likely to be treated and more likely to result in death.
      * **Changes within states:** E.g.: A falling number of users operating and dealing with the illegal market could make the market too "thin" and cause it to work less well. User may have difficulty accessing their usual substances, and may shift to new substances or new "coctails" with higher risk.
      * **Changes in the composition of the user population:** An aging population of users could face higher risks due to their age.

# The simulation model

## High level overview

The simulation consists of objects at three levels. Starting from the bottom:

1. **Individuals:** Individuals are characterized by their age and their history (their recent use level and which states they have been in). These objects have methods that determine their risk of overdose death, non-overdose death, and their current use level.
1. **States:** A state contains a set of individuals residing in that state. These individuals may also appear in one of the other sets within the state: The set of individuals that have died in the current period, the set of individuals that have died from OD in the current period, and the set of individuals that will shift to each of the other states at the end of the current period. Each state also affects use levels and the risks associated with any use level (e.g., in OMT a high level of use will have a lower risk of overdose). Each state has methods to identify who will be transferred to other states, as well as methods for updating the individuals. In practice, all individuals will be allocated across the three subclasses of States:
  * **NoTreatment** - Users who have never received, or who have exited from, treatment.
  * **DrugFreeTreatment** - Users who receive "traditional" forms of treatment for substance use
  * **OMT** - Users receiving some form of medication meant to replace their use of heroin.
 **Society.** The society contains the three states. It also contains methods for introducing new users into society (recruitment), for initializing the society, and for running the society and outputting simulation results.

 While this set-up has a certain level of complexity, it should hopefully make the final simulation model clean, easy to run, and easy to maintain.
 * Methods for initializing and running a simulation, outputting and visualizing results, etc. are in the Society state.
 * Modelling of (partly) observable shifts between the three states is handled at the state level. Since the individuals are held in a set within the state, the state-transfer risks are free to depend on any set of individual characteristics - but they are still methods of the state-object.
 * Modelling of use trajectories, heterogeneity in use, and death and overdose risks is modelled within the individual object. Updates are called from the state within which an individual resides, and the name of this state is passed along so that use and mortality risks are influenced by the current state.

 Note that the transfer risks from NoTreatment and DrugFreeTreatment into OMT has to be particularly flexibly, as we will need to model movements of users throughout a period in which OMT became gradually more available (age limits, waiting lines etc)

 ## Proposed calibration of model

 While this is likely to change over time as we develop the model, an initial guess at how this can be done is as follows:

 1. **Generate baseline situation.** Since we are attempting to explain the development in overdose mortality since the late nineties, a first step is to establish a situation similar to the one that existed prior to the introduction of OMT in Norway. To do this we gradually phase in new users while letting them age and shift between NoTreatment and DrugFreeTreatment. After a number of years, the earliest cohorts introduced will have aged so that the entire age interval is represented. A first goal is to find a set of parameters and functions that recreates the situation as it was prior to the introduction of OMT.
 2. **Add OMT.**
    1. Calibrate the transfers between the states so that the growth of members within the different states are plausible and consistent with what was observed.
    1. See what the model would predict in terms of mortality and overdose deaths as a result
    1. Define a set of hypotheses for how overdose mortality could remain high, and model these as separate simulation specifications. Examine how they would play out and affect the system, and to what extent the resulting effects can be examined in empirical data.
