from Modules.LatticeGasSimPcb import LatticeGasSimPcb
import matplotlib.pyplot as plt
import os
os.system('clear')

lgs = LatticeGasSimPcb(30,4)
lgs.animation1(frames=100,dpf=1,fps=4,filename="gasLatticePCB1.1")
lgs = LatticeGasSimPcb(30,4)
lgs.animation1(frames=100,dpf=1,fps=4,filename="gasLatticePCB1.2")
lgs = LatticeGasSimPcb(30,6)
lgs.animation1(frames=100,dpf=1,fps=4,filename="gasLatticePCB1.3")
lgs = LatticeGasSimPcb(30,8)
lgs.animation1(frames=100,dpf=1,fps=4,filename="gasLatticePCB1.4")
lgs = LatticeGasSimPcb(30,10)
lgs.animation1(frames=100,dpf=1,fps=4,filename="gasLatticePCB1.5")