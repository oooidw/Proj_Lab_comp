from Modules.LatticeGasSim import LatticeGasSim
import os
os.system('clear')

################################################
#--------------------TEST1---------------------#
################################################
"""lgs = LatticeGasSim(1000,500,rho=0.2,flowRate=-0.25,obs_type="barrier")
lgs.animation2(frames=50,dpf=30,ave_size=20,scale=500,filename="gasLattice_barr")"""


################################################
#--------------------TEST2---------------------#
################################################
"""lgs = LatticeGasSim(1000,500,0.2,flowRate=-0.28,obs_type="rombo")
lgs.animation2(frames=50,dpf=30,ave_size=20,scale=500,filename="gasLattice_romb")"""


################################################
#--------------------TEST3---------------------#
################################################
lgs = LatticeGasSim(1000,500,0.2,flowRate=-0.2,obs_type="cube")
lgs.animation2(frames=50,dpf=30,ave_size=20,scale=500,filename="/No_commit/gasLattice_cubeee")