import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from hexalattice.hexalattice import *
from Modules.modGaphics import *
from Modules.modulogl import modulogl as gl
from tqdm import tqdm, trange
import matplotlib.patches as patches

class LatticeGasSim:
    
    """
    Inizializza tutte le variabili globali utilizzate, genera le regole di collisione, inizializza il reticolo con
    la densità desiderata e con l'ostacolo desiderato.

    Lx : Dimensione x del reticolo
    Lx : Dimensione y del reticolo
    rho : Densità di particelle
    flowrate : Valore desiderato del flusso di particelle
    scale : Parametro che influenza il numero di inezioni per ottenere un certo flowrate
    seed : seed per la generazione di numeri casuali
    obs_type : tipo di ostacolo desiderato
    """
    def __init__(self,Lx,Ly,rho,flowRate=1,scale=4,seed=12345678,obs_type="barrier"):
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
        self.N = int(Lx*Ly*7*rho)
        self.Lx = Lx
        self.Ly = Ly
        self.flowRate = flowRate
        self.scale = scale
        self.format = format
        self.seed = (seed // 10 ** np.arange(7,-1,-1)[:] % 10).astype(dtype=int,order='F')
        self.rng = np.random.default_rng(seed=seed)

        # Generazione regole collisione
        gl.gen_rules(self.N,self.flowRate,self.scale,self.seed)

        # Inizializzazione del lattice
        self.lattice = np.zeros((self.Ly,self.Lx),dtype=np.uint8)
        self.newLattice = np.zeros((self.Ly,self.Lx),dtype=np.uint8)
        self.histLattice = np.zeros((self.Ly,self.Lx),dtype=np.uint8)
        
        # Barriere
        self.lattice[1,:] = self.B
        self.lattice[self.Ly-2,:] = self.B
        
        # Creazione delle particelle iniziali
        x,y = self.rng.integers(2,self.Lx-2,self.N),self.rng.integers(2,self.Ly-2,self.N)
        self.lattice[y,x] = 127
        self.lattice[5,5] = 1

        # Generazione dell'ostacolo
        self.obs_type = obs_type
        if self.obs_type == "barrier":   # Primo tipo di ostacolo
            self.propy1, self.propy2 =  int(self.Ly*.2),int(self.Ly*.8)               # | dimensioni della barriera in proporzione alla dimensione del lattice
            self.propx1 = int(self.Lx*0.3)                                              # |
            self.lattice[self.propy1:self.propy2,self.propx1] = self.B
        elif self.obs_type == "rombo":   # Secondo tipo di ostacolo
            self.propy1, self.propy2 = int(self.Lx*0.3),int(self.Lx*0.6)                    # | dimensioni del rombo in proporzione alle dimensioni del lattice
            self.propx1 = int(self.Ly*.5)                                                   # |
            ii =   self.propx1                                          
            for i in range(self.propy1,self.propy2):
                if i<=(self.propy2-self.propy1)/2+self.propy1 : 
                    self.lattice[ii:2*(i-self.propy1)+ii,i] = self.B
                    ii -= 1
                else:
                    self.lattice[ii:2*(self.propy2-i)+ii,i] = self.B
                    ii += 1 
        elif self.obs_type == "cube": # Terzo tipo di ostacolo
            self.propx1, self.propx2 =  int(self.Ly*.1),int(self.Ly*.9)               # | dimensioni della barriera in proporzione alla dimensione del lattice
            self.propy1, self.propy2 =  int(self.Lx*0.3),int(self.Lx*0.4)             # |
            self.lattice[self.propx1:self.propx2,self.propy1:self.propy2] = self.B

        self.vxTotal = []

    """
    Tramite la funzione count_lattice() genera un array per colorare il reticolo, barr è il colore della barriera 
    e parr quello delle particelle, entrambi in formato RGB.
    """
    def draw_colors(self):
        barr = np.array([1.,0.,0.])
        parr = np.array([0.,0.,1.])
        return gl.count_lattice(barr,parr,self.lattice)


    """
    Funzione chiamata per progredire con la simulazione.

    n : indica il numero di step che si desidera simulare
    """
    def simulation(self,n):
        for i in range(n):
            self.lattice = gl.update_lattice(self.lattice).astype(dtype=np.uint8,order='F')


    """
    Funzione che genera un'animazione della simulazione. Si visualizza l'intero reticolo e tutte le particelle al suo interno.
    Un colore più intenso significa più particelle in quel sito del reticolo.

    frames : il numero di frame da disegnare
    dpf : il numero di step della simulazione per ogni frame
    dpi : dpi dell'immagine se si sceglie il formato gif
    filename : nome del file di output dell'animazione
    formato : formato del file di output (gif o mp4)
    """
    def animation1(self,frames,dpf=30,dpi=200,filename="Sim",format="gif"):
        def update(frame): 
            colors = self.draw_colors() 
            self.simulation(dpf)

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
            ani.save(filename="/root/MyCode/Lab_Comp/Proj/Images/"+filename+".gif", writer="pillow",dpi=dpi,fps=10)
        elif format == "mp4":
            Writer = animation.writers['ffmpeg']
            writer = Writer(fps=20, metadata=dict(artist='Me'), bitrate=8000)
            ani.save(filename="/root/MyCode/Lab_Comp/Proj/Images/"+filename+".mp4", writer=writer)


    """
    Funzione che genera un'animazione della simulazione. Questa visualizza le velocità tramite vettori
    calcolati tramite coarse grained average.

    frames : il numero di frame da disegnare
    dpf : il numero di step della simulazione per ogni frame
    dpi : dpi dell'immagine se si sceglie il formato gif
    filename : nome del file di output dell'animazione
    formato : formato del file di output (gif o mp4)
    ave_size : dimensioni del quadrato per coarse grained average
    scale : parametro per regolare le dimensioni dei vettori
    """
    def animation2(self,frames,dpf=30,dpi=200,filename="Sim",format="gif",ave_size=10,scale=5):
            
        def update(frame):
            
            a = gl.vel_lattice(dx,dy,self.lattice)           

            vx = -a[0:dy,:]/(ave_size)
            
            vy = -a[dy:,:]/(ave_size)

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
        
        # Plot dell'ostacolo
        if self.obs_type == "barrier":
            axs.plot([self.propx1]*2,[self.propy1, self.propy2])
        elif self.obs_type == "rombo":
            x = [self.propy1, self.propy1*3/2, int(self.Lx*0.6),  self.propy1*3/2]
            y = [self.propx1, self.propx1*3/2, self.propx1, self.propx1*1/2]
            axs.add_patch(patches.Polygon(xy=list(zip(x,y)), fill=True,color='C0'))
        elif self.obs_type == "cube":
            y = [self.propx1, self.propx1, self.propx2,  self.propx2]
            x = [self.propy1, self.propy2, self.propy2, self.propy1]
            axs.add_patch(patches.Polygon(xy=list(zip(x,y)), fill=True,color='C0'))
     
        
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
