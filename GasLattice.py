from Modules.LatticeGasSim import LatticeGasSim
import os
os.system('clear')

################################################
# Codice utilizzato per generare gli esempi 
# su github
################################################

lgs = LatticeGasSim(1000,500,rho=0.2,flowRate=-0.25,obs_type="barrier")
lgs.animation2(frames=200,dpf=30,ave_size=20,scale=500,filename="gasLattice_barr")
lgs = LatticeGasSim(1000,500,rho=0.2,flowRate=-0.1,obs_type="barrier")
lgs.animation2(frames=200,dpf=30,ave_size=20,scale=400,filename="gasLattice_barr2")
lgs = LatticeGasSim(1000,500,rho=0.2,flowRate=-0.05,obs_type="barrier")
lgs.animation2(frames=200,dpf=30,ave_size=20,scale=300,filename="gasLattice_barr3")

lgs = LatticeGasSim(1000,500,0.2,flowRate=-0.25,obs_type="rombo")
lgs.animation2(frames=200,dpf=30,ave_size=20,scale=500,filename="gasLattice_romb")
lgs = LatticeGasSim(1000,500,rho=0.2,flowRate=-0.1,obs_type="rombo")
lgs.animation2(frames=200,dpf=30,ave_size=20,scale=400,filename="gasLattice_romb2")
lgs = LatticeGasSim(1000,500,rho=0.2,flowRate=-0.05,obs_type="rombo")
lgs.animation2(frames=200,dpf=30,ave_size=20,scale=300,filename="gasLattice_romb3")

lgs = LatticeGasSim(1000,500,0.2,flowRate=-0.25,obs_type="cube")
lgs.animation2(frames=200,dpf=30,ave_size=20,scale=500,filename="gasLattice_cube")
lgs = LatticeGasSim(1000,500,0.2,flowRate=-0.1,obs_type="cube")
lgs.animation2(frames=200,dpf=30,ave_size=20,scale=500,filename="gasLattice_cube2")