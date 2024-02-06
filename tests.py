from Modules.LatticeGasSim import LatticeGasSimPcb
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
os.system('clear')

# Animazione dell'istogramma
lgs = LatticeGasSimPcb(40,4)
lgs.animation1(frames=200,dpf=3,fps=1,filename="/No_commit/test")
plt.clf()



figure, axs = plt.subplots()
def update(frames):
    plt.cla()
    axs.hist(lgs.havex[frames])
    axs.set_title(frames*3)

ani = animation.FuncAnimation(figure, func = update, frames = 200)

plt.show()

# Plot del grafico
plt.xlabel(r"Densità $\rho$")
plt.ylabel("tempo di equilibrazione")
plt.plot([0.027,0.06,0.107,0.24,0.24,0.427,0.667,0.96],[140,100,90,75,68,60,60,50])
plt.errorbar([0.027,0.06,0.107,0.24,0.24,0.427,0.667,0.96],[140,100,90,75,68,60,60,50],marker="x",linestyle='')

plt.show()