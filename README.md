# CryoSkywater130nm_CorrectedForNgspice

#Downloading_Volare
First, ensure Volare is properly set up (I did this by creating a seperate file titled skywater130nm where I placed all the things downloaded from volare (which should be 3 top files: volare, sky130A, sky130B.) 
My path essentially looked like /home/<user>/skywater130nm/volare...)

To download volare, I used the following:

```
pip install volare

export PDK_ROOT="/home/<your_username>/<desired_PDK_directory>"

volare ls-remote --pdk sky130
# Lists all available versions of the Sky130 PDK

volare enable --pdk sky130 a918dc7c8e474a99b68c85eb3546b4ed91fe9e7b
# This version from 10/08/2024 was used for 77K PDK development
```

#Downloading_Ngspice

I used jupyter notebooks for this, so that is the setup I will show. However, just make sure version 41 of ngspice is installed and it should work.
This is the setup I used, and I just made sure sims were run in spice_env:
```
  conda activate spice_env
  conda install -c conda-forge ngspice=41
  which ngspice
  ngspice --version
```

#Enviornment_Setup
In order to correctly set up the 77k file to work with the rest of volare, you will want to place sky130_fd_pr__nfet_01v8_lvt__tt_77k.corner.spice in the following directory:
```
skywater130nm/volare/sky130/versions/a918dc7c8e474a99b68c85eb3546b4ed91fe9e7b/sky130A/libs.ref/sky130_fd_pr/spice
```
(the ordiginal sky130_fd_pr__nfet_01v8_lvt__tt_77k.corner.spice was compressed by Mystic. To use this with NGspice, you can either use the translated script or you can translate the original 
script using the translation code in the repo. You will also want to replace the include with your own directory.)

Once the correct nfet file has been placed in the directory, you will want to update the sky130.lib.spice file (/home/<user>/skywater130nm/volare/sky130/versions/a918dc7c8e474a99b68c85eb3546b4ed91fe9e7b/sky130A/libs.tech/ngspice/sky130.lib.spice)
To do this, insert the following code in sky130.lib.spice under '******* SkyWater sky130 model library *********':

```
* Typical corner (tt) at 77K
.lib tt_77k
.param mc_mm_switch=0
.param mc_pr_switch=0
.param my_gauss = 0
.param m = 1
.include "/home/oliviag/skywater130nm/volare/sky130/versions/a918dc7c8e474a99b68c85eb3546b4ed91fe9e7b/sky130A/libs.ref/sky130_fd_pr/spice/sky130_fd_pr__nfet_01v8_lvt__tt_77k.corner.spice"
*.include "../cells/pfet_01v8_lvt/77k_models/sky130_fd_pr__pfet_01v8_lvt__tt_77k.corner.spice"

.include "/home/<user>/skywater130nm/volare/sky130/versions/a918dc7c8e474a99b68c85eb3546b4ed91fe9e7b/sky130A/libs.ref/sky130_fd_pr/spice/sky130_fd_pr__nfet_01v8_lvt__mismatch.corner.spice"
.include "/home/<user>/skywater130nm/volare/sky130/versions/a918dc7c8e474a99b68c85eb3546b4ed91fe9e7b/sky130A/libs.ref/sky130_fd_pr/spice/pfet_01v8_lvt/sky130_fd_pr__pfet_01v8_lvt__mismatch.corner.spice"

.include "r+c/res_typical__cap_typical.spice"
.include "r+c/res_typical__cap_typical__lin.spice"

* Special cells
.include "corners/tt/specialized_cells.spice"


.endl
```

After this, to use the pdk at 77k, just change the .lib declaration in the ngspice files from tt to tt_77k!

#Running_NGSpice_Sims

The ngspice simulation can be run just from the terminal. Inside the simulation folder in the repo, you will find 4 .spice files: 
- vds_sweep_IV.spice : Sweeps VDS with constant VGS
- vgs_sweep_IV.spice : Sweeps VGS with constant VDS
- vgs_sweep_varVDS.spice : Sweeps VGS several times over a set of constant VDS
- vds_sweep_varVGS.spice : Sweeps VDS several times over a set of constant VGS

These can be run by typing ```ngspice -b <desiredSim.spice>``` in the terminal while in the simulation directory. 

To plot the results, use plotting-spice.ipynb, where there are several different plotting methods depending on which simulation was run.
(note: if you set ngspice in a specific enviornment like spice_env, make sure it is active while trying to run the simulation)

  

