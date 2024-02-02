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
  <img width="600" src="https://github.com/oooidw/Proj_Lab_comp/blob/main/Images/gasLattice_barr.gif">
</p>

Nel sencondo caso utilizziamo invece LatticeGasSimPcb e animation1 in tal modo:
```sh
lgs = LatticeGasSimPcb(30,4)
lgs.animation1(frames=100,dpf=1,fps=4,filename="gasLatticePCB1.1")
```
per ottenere:
<p align="center">
  <img width="600" src="https://github.com/oooidw/Proj_Lab_comp/blob/main/Images/gasLatticePCB1.1.gif">
</p>

## Parametri aggiuntivi
```sh
lgs = LatticeGasSim(
      Lx                             # Dimensione x del reticolo
      Lx                             # Dimensione y del reticolo
      rho        = 0.2               # Densità di particelle
      flowrate   = 0.2               # Valore desiderato del flusso di particelle
      scale      = 4                 # Parametro che influenza il numero di inezioni per ottenere un certo flowrate
      seed       = 12345678          # seed per la generazione di numeri casuali
      obs_type   = "barrier"         # tipo di ostacolo desiderato (barriera, quadrato o rombo)
)
```
```sh
lgs = LatticeGasSimPcb(
      L                              # Lato del reticolo L*L
      b                              # Lato del quadrato contenente le particelle iniziali
      seed       = 12345678          # seed per la generazione di numeri casuali
)
```
```sh
lgs.animation1(
      frames                         # il numero di frame da disegnare
      dpf        = 30                # il numero di step della simulazione per ogni frame
      dpi        = 200               # dpi dell'immagine se si sceglie il formato gif
      filename   = "Sim"             # nome del file di output dell'animazione
      formato    = "gif"             # formato del file di output (gif o mp4)
)
```
```sh
lgs.animation1(
      frames                         # il numero di frame da disegnare
      dpf        = 30                # il numero di step della simulazione per ogni frame
      dpi        = 200               # dpi dell'immagine se si sceglie il formato gif
      filename   = "Sim"             # nome del file di output dell'animazione
      formato    = "gif"             # formato del file di output (gif o mp4)
      ave_size   = 10                # dimensioni del quadrato per coarse grained average
      scale      = 5                 # parametro per regolare le dimensioni dei vettori
)
```
