from Modules.LatticeGasSim import LatticeGasSimPcb
import os
os.system('clear')


################################################
# Codice utilizzato per generare gli esempi 
# su github
################################################

lgs = LatticeGasSimPcb(30,2)
lgs.animation1(frames=200,dpf=3,fps=2,filename="gasLatticeL30b2")

lgs = LatticeGasSimPcb(30,4)
lgs.animation1(frames=200,dpf=3,fps=2,filename="gasLatticeL30b4")

lgs = LatticeGasSimPcb(30,6)
lgs.animation1(frames=200,dpf=3,fps=2,filename="gasLatticeL30b6")

lgs = LatticeGasSimPcb(30,8)
lgs.animation1(frames=200,dpf=3,fps=2,filename="gasLatticeL30b8")

lgs = LatticeGasSimPcb(30,10)
lgs.animation1(frames=200,dpf=3,fps=2,filename="gasLatticeL30b10")

lgs = LatticeGasSimPcb(10,4)
lgs.animation1(frames=200,dpf=3,fps=2,filename="gasLatticeL10b4")

lgs = LatticeGasSimPcb(20,4)
lgs.animation1(frames=200,dpf=3,fps=2,filename="gasLatticeL20b4")

lgs = LatticeGasSimPcb(40,4)
lgs.animation1(frames=200,dpf=3,fps=2,filename="gasLatticeL40b4")