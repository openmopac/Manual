Starting with the reactants and produces, the first step is to move the two geometries towards each other using Locate_TS.mop

Then the two resulting geometries, "Locate_TS bias=20.0 first.mop" and "Locate_TS bias=20.0 second.mop" are used in starting a SADDLE calculation, Saddle_TS.mop.  This gives a good approximation to the transition state.

In a final job, "Dimethylenebenzene Dihydrocyclobutabenzene IRC.mop" the transition state geometry is refined, and an IRC run.
