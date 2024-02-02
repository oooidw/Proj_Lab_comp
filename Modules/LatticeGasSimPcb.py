import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from hexalattice.hexalattice import *
import time
from Modules.modGaphics import *
from Modules.modulogl import modulogl as gl
from tqdm import tqdm, trange
import matplotlib.patches as patches

class LatticeGasSimPcb:

    def __init__(self,Lx,b,seed=12345678):
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
        self.b = b
        self.N = b*b*6
        self.Lx = Lx
        self.Ly = Lx
        self.flowRate = 1
        self.scale = 4
        self.format = format
        self.seed = (seed // 10 ** np.arange(7,-1,-1)[:] % 10).astype(dtype=int,order='F')
        self.rng = np.random.default_rng(seed=seed)

        # Generazione regole collisione
        gl.gen_rules(self.N,self.flowRate,self.scale,self.seed)

        # Inizializzazione del lattice
        self.lattice = np.zeros((self.Ly+2,self.Lx),dtype=np.uint8)
        self.newLattice = np.zeros((self.Ly+2,self.Lx),dtype=np.uint8)
        
        # Creazione delle particelle iniziali
        x,y = self.rng.integers(2,self.Lx-2,self.N),self.rng.integers(2,self.Ly-2,self.N)
        Lhalf = int((Lx-1)/2)
        self.lattice[int(Lhalf-b/2):int(Lhalf+b/2),int(Lhalf-b/2):int(Lhalf+b/2)] = 127

        self.vxTotal = []
        self.vyTotal = []


    def lattice_ini(self):
        self.fig, self.ax = plt.subplots()
        hex_centers, _ = create_hex_grid(nx=self.Lx,ny=self.Ly,do_plot=False,align_to_origin=False)
        self.x_hex_coords = hex_centers[:, 0]
        self.y_hex_coords = hex_centers[:, 1]
        c = self.draw_colors()
        plot_single_lattice_custom_colors(self.x_hex_coords, self.y_hex_coords,face_color=c,edge_color=[1,1,1],min_diam=1,plotting_gap=0,rotate_deg=0,h_ax=self.ax)
        plt.show()       

    
    def draw_colors(self):
        barr = np.array([1.,0.,0.])
        parr = np.array([0.,0.,1.])
        return gl.count_lattice(barr,parr,self.lattice)


    def simulation(self,n):
        for i in range(n):
            self.lattice = gl.update_lattice_pcb(self.lattice).astype(dtype=np.uint8,order='F')
            self.vxTotal.append(gl.vxtotal)
            self.vyTotal.append(gl.vytotal)


    def animation1(self,frames,dpf=30,dpi=80,filename="Sim",format="gif",fps=10):
        
        def update(frame): 
            colors = self.draw_colors() 
            self.simulation(dpf)
            axs.set_title("time step "+str(frame*dpf))

            p_bar.update()
            if frame==frames-1:
                tqdm.close(p_bar)
                print("Salvataggio...")                
            return collection.set_facecolors(colors)

        # Parameters
        x_dim = self.Lx
        y_dim = self.Ly
        diam = 1

        
        # Generazione dell'animazione
        figure, axs = plt.subplots()
        #figure.set_size_inches(12, 12)
        
        # Generazione degli esagoni
        print("Creazione lattice...")        
        centers, _ = create_hex_grid(nx = x_dim, ny = y_dim, min_diam = diam,align_to_origin=False)
        
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
        
        if format == "gif":
            ani.save(filename="/root/MyCode/Lab_Comp/Proj/Images/"+filename+".gif", writer="pillow",dpi=dpi,fps=fps)
        elif format == "mp4":
            Writer = animation.writers['ffmpeg']
            writer = Writer(fps=20, metadata=dict(artist='Me'), bitrate=8000)
            ani.save(filename="/root/MyCode/Lab_Comp/Proj/Images/"+filename+".mp4", writer=writer)


    def animation2(self,frames,dpf=30,dpi=200,filename="Sim",format="gif",ave_size=10,scale=5):
            
        def update(frame):
            
            a = gl.vel_lattice(dx,dy,self.lattice)           

            vx = a[0:dy,:]/(ave_size)
            
            vy = a[dy:,:]/(ave_size)

            Q.set_UVC(vx,vy)

            self.simulation(dpf)           

            self.vxTotal.append(gl.vxtotal)

            p_bar.update()
            if frame==frames-1:
                tqdm.close(p_bar)
                print("Salvataggio...")
        
        # Generazione del plot
        figure, axs = plt.subplots()
        axs.set_aspect('equal')
        #figure.set_size_inches(12, 12)        

        #--Inizializzazione dell'animazione--
        print("Inizializzazione...")  
        dx = int(self.Lx/ave_size)
        dy = int(self.Ly/ave_size)
        X, Y = np.meshgrid(np.linspace(0,self.Lx,dx), np.linspace(0,self.Ly,dy))
        a = gl.vel_lattice(dx,dy,self.lattice)   
        vx = a[0:dy,:]/(ave_size)
        vy = a[dy:,:]/(ave_size)
        Q = axs.quiver(X, Y, vx, vy,angles='xy',scale=scale, width=0.0008)    
     
        
        # Animazione
        print("Inizio simulazione...")
        p_bar = tqdm(range(frames),leave=True)        
        ani = animation.FuncAnimation(figure, func = update, frames = frames)


        # Salvataggio
        if format == "gif":
            ani.save(filename="/root/MyCode/Lab_Comp/Proj/Images/"+filename+".gif", writer="pillow",dpi=dpi,fps=5)
        elif format == "mp4":
            Writer = animation.writers['ffmpeg']
            writer = Writer(fps=5, metadata=dict(artist='Me'), bitrate=8000)
            ani.save(filename="/root/MyCode/Lab_Comp/Proj/Images/"+filename+".mp4", writer=writer)
