The first calculation, to find the highest point on the reaction path, is unusually complicated.  Using the simple strategy of dragging a hydrogen atom from C1 to C2, was not suitable because the resulting potential energy surface is discontinuous.  To avoid this problem, the geometry was re-defined as follows:

All atoms except C2 were defined in Cartesian coordinates. These atoms would not be used in defining the reaction path, so it's simpler to just have them in Cartesian coordinates.

A dummy atom is defined in internal coordinates relative to C1.

Using symmetry the middle carbon atom is defined as being equidistant to C1 and the dummy atom.

The hydrogen atom that moves is then defined as being somewhere along a straight line from the dummy atom to C1.

The reaction path then consists of steadily moving the dummy atom away from C1; this maps out a well-behaved path, one that does not have a discontinuity.

When this job is run, the highest point is used as an approximation to the transition state.  Refinement of the transition state requires the symmetry and dummy atom to be deleted.  This is accomplished by keywords XYZ and OPT.

All other steps are done in the conventional manner.