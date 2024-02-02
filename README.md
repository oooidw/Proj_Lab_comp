# Liquid flow simulation with lattice gas model
Vediamo qui l'utilizzo delle classi LatticeGasSim per la simulazione del flusso di un fluido

## Dipendenze
* Matplotlib
* Numpy
* tqdm
* hexalattice

## Esempi
Importiamo inanzitutto il modulo python
```sh
from Modules.LatticeGasSim import *
```
Vediamo due esempi. Nel primo caso usiamo LatticeGasSim e animation2 per visualizzare il flusso del fluido:
```sh
lgs = LatticeGasSim(1000,500,0.2,flowRate=-0.2,obs_type="barrier")
lgs.animation2(frames=50,dpf=30,ave_size=20,scale=500,filename="gasLattice_barr")
```
che genera la seguente animazione:
<p align="center">
  <img width="600" src="https://github.com/oooidw/Proj_Lab_comp/blob/main/Images/gasLattice_cube.gif">
</p>
Nel sencondo caso utilizziamo invece LatticeGasSimPcb e animation1 in tal modo:
lgs = LatticeGasSimPcb(30,4)
lgs.animation1(frames=100,dpf=1,fps=4,filename="gasLatticePCB1.1")
per ottenere:
<p align="center">
  <img width="600" src="https://github.com/oooidw/Proj_Lab_comp/blob/main/Images/gasLatticePCB1.1gif">
</p>
