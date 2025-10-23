load CVD-0013226.pdb  
/cmd.load('CVD-0013226.pdb', quiet=0) 
select ligand, resn LIG
show sticks, ligand
set_bond stick_radius, 0.15, ligand
show spheres, ligand
alter ligand, vdw=0.3
show surface
set_view (\
     0.603444636,    0.399759054,   -0.689961195,\
    -0.120104626,    0.900954306,    0.416962743,\
     0.788308322,   -0.168745756,    0.591687024,\
     0.000005022,    0.000005554,  -61.020805359,\
    11.700496674,   -2.072804689,   17.543632507,\
  -488.979614258,  618.319946289,  -20.000000000 )
set surface_quality, 1
clip slab, 1000
select opt, (stereo "R" or stereo "S") and resi 452
label opt, stereo
set label_color, black, opt
set label_size, 30
deselect








