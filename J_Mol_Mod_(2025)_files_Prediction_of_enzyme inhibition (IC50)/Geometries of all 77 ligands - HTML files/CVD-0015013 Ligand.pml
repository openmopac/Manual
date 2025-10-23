load CVD-0015013 Ligand.pdb  
/cmd.load('CVD-0015013 Ligand.pdb', quiet=0)  
REM select ligand, resn LIG
select ligand, all
show sticks, ligand
set_bond stick_radius, 0.15, ligand
show spheres, ligand
alter ligand, vdw=0.3
select fluorine, (name F*)
alter fluorine, vdw=0.4
center ligand
rebuild
set_view (\
     0.759137332,    0.248964548,   -0.601437151,\
    -0.171940967,    0.967844129,    0.183614165,\
     0.627811790,   -0.035976127,    0.777532041,\
     0.000000000,    0.000000000, -111.642776489,\
    12.428121567,   -1.754789829,   18.284368515,\
    88.020019531,  135.265533447,  -20.000000000 )
show surface
set_view (\
     0.603444636,    0.399759054,   -0.689961195,\
    -0.120104626,    0.900954306,    0.416962743,\
     0.788308322,   -0.168745756,    0.591687024,\
     0.000005022,    0.000005554,  -61.020805359,\
    11.700496674,   -2.072804689,   17.543632507,\
  -488.979614258,  618.319946289,  -20.000000000 )
center
set surface_quality, 1
clip slab, 1000
select opt, (stereo "R" or stereo "S") and resi 452
label opt, stereo
set label_color, black, opt
set label_size, 30
deselect










