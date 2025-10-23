This reaction involves HNC isomerizing to HCN. A normal first step, shown here with HCN.mop and HNC.mop, is to optimize the geometries of the reactant and product.  

In this particular case, both HNC and HCN are perfectly linear; this would confuse the transition state location routine SADDLE, so to avoid that, both reactant and product are moved "by hand" in the direction of the transition state.  This is done by displacing the nitrogen atom in both HCN and HNC half an Angstrom in the "y" direction so as to make bent molecules.  To avoid the geometry optimizer from relaxing the molecules and making them linear once more, both molecules have had their bond-lengths shortened.  This puts a strong constraint on them so that they appear to be already on the slopes of the reaction barrier. These systems are named "HNC for TS.mop" and "HCN for TS.mop".

Transition state location for the HNC - HCN system is unusual in that all atoms are involved in bond-making - bond-breaking.  This means that the usual transition state refinement, consisting of alternating energy minimization and gradient minimization, has been automatically replaced by gradient minimization only.

The name of the data set for locating the transition state is "HCN-HNC.mop".  It uses the following keywords:

GEO_DAT="HCN for TS.arc"  For this type of calculation, it is easier to have the reactants and products as separate files.
GEO_REF="HNC for TS.arc"
SADDLE   Use the SADDLE transition state locator.

To visualize the Intrinsic Reaction Coordinate, an IRC=1* calculation is run with HTML, and, to produce a graph with constant changes in geometry X-PRIORITY=0.05 is used.  This is shown in "HCN-HNC_IRC.mop".


To visualize the Dynamic Reaction Coordinate, IRC=1* and DRC are run with HTML, and, to produce a graph with constant changes in time T-PRIORITY=0.5 is used.  This is shown in "HCN-HNC_DRC.mop".


  