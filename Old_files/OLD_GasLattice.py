import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from hexalattice.hexalattice import *
import time
from Modules.modGaphics import *
from Modules.modulogl import modulogl as gl
from tqdm import tqdm, trange


class LatticeGasSim:

    def __init__(self,L,rho,frames,dpi=80,filename="Sim",format="gif",flowRate=1,scale=4,seed=12345678):
        # Abbreviazioni per le direzioni
        self.RI = 1      
        self.RD = 2
        self.LD = 4
        self.LE = 8
        self.LU = 16
        self.RU = 32        
        self.S = 64
        self.B = 128
        
        # Parametri iniziali
        self.rho = rho
        self.N = int(L*L*7*rho)
        self.L = L
        self.flowRate = flowRate
        self.scale = scale
        self.format = format
        self.seed = (seed // 10 ** np.arange(7,-1,-1)[:] % 10).astype(dtype=int,order='F')
        self.rng = np.random.default_rng(seed=seed)


        # Generazione regole collisione
        gl.gen_rules(self.N,self.flowRate,self.scale,self.seed)

        # Inizializzazione del lattice
        self.lattice = np.zeros((self.L,self.L),dtype=np.uint8)
        self.newLattice = np.zeros((self.L,self.L),dtype=np.uint8)
        
        # Barriera sopra e sotto
        self.lattice[1,:] = self.B
        self.lattice[self.L-2,:] = self.B

        #Creazione di una barriera e delle particelle iniziali
        x,y = self.rng.integers(2,self.L-2,self.N),self.rng.integers(2,self.L-2,self.N)
        self.lattice[x,y] = 127
        self.lattice[60:130,120] = self.B

        # Inizializzazione per l'animazione
        self.frames = frames
        self.dpi = dpi
        self.filename = filename


    def lattice_ini(self):
        self.fig, self.ax = plt.subplots()
        hex_centers, _ = create_hex_grid(nx=self.L,ny=self.L,do_plot=False,align_to_origin=False)
        self.x_hex_coords = hex_centers[:, 0]
        self.y_hex_coords = hex_centers[:, 1]
        c = self.draw_colors()
        plot_single_lattice_custom_colors(self.x_hex_coords, self.y_hex_coords,face_color=c,edge_color=[1,1,1],min_diam=1,plotting_gap=0,rotate_deg=0,h_ax=self.ax)
        plt.show()       

    
    def draw_colors(self):
        barr = np.array([1.,0.,0.])
        parr = np.array([0.,0.,1.])
        return gl.count_lattice(self.lattice,barr,parr)


    def animation(self):
        
        def update(frame):
            colors = self.draw_colors() 
            self.lattice = gl.update_lattice(self.lattice,self.L).astype(dtype=np.uint8,order='F')

            p_bar.update()
            if frame==frames-1:
                tqdm.close(p_bar)
                print("Salvataggio...")                
            return collection.set_facecolors(colors)

        # Parameters
        x_dim = self.L
        y_dim = self.L
        diam = 1
        frames = self.frames
        
        # Generazione dell'animazione
        figure, axs = plt.subplots()
        figure.set_size_inches(12, 12)
        
        print("Creazione lattice...")        
        centers, _ = create_hex_grid(nx = x_dim, ny = y_dim, min_diam = diam)
        
        polygons = [mpatches.RegularPolygon((x, y), numVertices = 6, radius = diam / np.sqrt(3)) for x, y in zip(centers[:, 0], centers[:, 1])]
        collection = PatchCollection(polygons)
        axs.add_collection(collection)

        axs.set_aspect('equal')
        axs.axis([
            centers[:, 0].min() - 2 * diam,
            centers[:, 0].max() + 2 * diam,
            centers[:, 1].min() - 2 * diam,
            centers[:, 1].max() + 2 * diam,
        ])

        # Animate
        print("Inizio simulazione...")
        p_bar = tqdm(range(frames),leave=True)
        ani = animation.FuncAnimation(figure, func = update, frames = frames)
        #plt.show()
        if self.format == "gif":
            ani.save(filename="/root/MyCode/Lab_Comp/Proj/Images/"+self.filename+".gif", writer="pillow",dpi=self.dpi,fps=10)
        elif self.format == "mp4":
            Writer = animation.writers['ffmpeg']
            writer = Writer(fps=20, metadata=dict(artist='Me'), bitrate=8000)
            ani.save(filename="/root/MyCode/Lab_Comp/Proj/Images/"+self.filename+".mp4", writer=writer)

import os
os.system('clear')


lgs = LatticeGasSim(250,0.1,1000,flowRate=5)

lgs.animation()
