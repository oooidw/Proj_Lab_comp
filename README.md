# Liquid flow simulation with lattice gas model
Vediamo qui l'utilizzo delle classi LatticeGasSim per la simulazione del flusso di un fluido

## Dipendenze
* Matplotlib
* Numpy
* tqdm
* hexalattice

## Esempi
Vediamo due esempi:
```sh
lgs = LatticeGasSim(1000,500,0.2,flowRate=-0.2,obs_type="barrier")
lgs.animation2(frames=50,dpf=30,ave_size=20,scale=500,filename="gasLattice_barr")
```
che genera la seguente animazione:
<p align="center">
  <img width="600" src="https://github.com/oooidw/Proj_Lab_comp/blob/main/Images/gasLattice_cube.gif">
</p>
