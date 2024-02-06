import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from hexalattice.hexalattice import *
from Modules.modGaphics import *
from Modules.modulogl import modulogl as gl
from tqdm import tqdm, trange
import matplotlib.patches as patches

class LatticeGasSim:
    
    def __init__(self,Lx,Ly,rho=0.2,flowRate=0.2,scale=4,seed=12345678,obs_type="barrier"):
        """
        Inizializza tutte le variabili globali utilizzate, genera le regole di collisione, inizializza il reticolo con
        la densità desiderata e con l'ostacolo desiderato.

        Args:
        Lx - Dimensione x del reticolo
        Lx - Dimensione y del reticolo
        rho - Densità di particelle
        flowrate - Valore desiderato del flusso di particelle
        scale - Parametro che influenza il numero di inezioni per ottenere un certo flowrate
        seed - seed per la generazione di numeri casuali
        obs_type - tipo di ostacolo desiderato
        """

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
        
        # Barriere sopra e sotto
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
            self.propx1, self.propx2 =  int(self.Ly*.3),int(self.Ly*.6)               # | dimensioni della barriera in proporzione alla dimensione del lattice
            self.propy1, self.propy2 =  int(self.Lx*0.3),int(self.Lx*0.8)             # |
            self.lattice[self.propx1:self.propx2,self.propy1:self.propy2] = self.B


    def simulation(self,n):
        """
        Funzione chiamata per progredire con la simulazione.

        Args:
        n - indica il numero di step che si desidera simulare
        """

        for i in range(n):
            self.lattice = gl.update_lattice(self.lattice).astype(dtype=np.uint8,order='F')

  
    def animation2(self,frames,dpf=30,dpi=200,filename="Sim",format="gif",ave_size=10,scale=5):
        """
        Funzione che genera un'animazione della simulazione. Questa visualizza le velocità tramite vettori
        calcolati tramite coarse grained average.

        Args:
        frames - il numero di frame da disegnare
        dpf - il numero di step della simulazione per ogni frame
        dpi - dpi dell'immagine se si sceglie il formato gif
        filename - nome del file di output dell'animazione
        formato - formato del file di output (gif o mp4)
        ave_size - dimensioni del quadrato per coarse grained average
        scale - parametro per regolare le dimensioni dei vettori
        """

        # Funzione che genere il nuovo frame dell'animazione
        def update(frame):              
            
            # Calcolo delle velocità
            a = gl.vel_lattice(dx,dy,self.lattice)   
            vx = -a[0:dy,:]/(ave_size)
            vy = -a[dy:,:]/(ave_size)

            # Aggiornamento dei vettori velocità
            Q.set_UVC(vx,vy)

            # Avanzamento della simulazione
            self.simulation(dpf)           

            # Cambio del titolo
            axs.set_title("time step "+str(frame*dpf))

            p_bar.update()
            if frame==frames-1:
                tqdm.close(p_bar)
                print("Salvataggio...")
        
        # Generazione del plot
        figure, axs = plt.subplots()
        axs.set_aspect('equal')        

        # Inizializzazione dell'animazione
        print("Inizializzazione...")  
        dx = int(self.Lx/ave_size)
        dy = int(self.Ly/ave_size)
        X, Y = np.meshgrid(np.linspace(0,self.Lx,dx), np.linspace(0,self.Ly,dy))
        a = gl.vel_lattice(dx,dy,self.lattice)   
        vx = a[0:dy,:]/(ave_size)
        vy = a[dy:,:]/(ave_size)
        Q = axs.quiver(X, Y, vx, vy,angles='xy',scale=scale, width=0.0008)    
        axs.set_xlabel("x")
        axs.set_ylabel("y")
        
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
            ani.save(filename="Examples/"+filename+".gif", writer="pillow",dpi=dpi,fps=5)
        elif format == "mp4":
            Writer = animation.writers['ffmpeg']
            writer = Writer(fps=5, metadata=dict(artist='Me'), bitrate=8000)
            ani.save(filename="Examples/"+filename+".mp4", writer=writer)



class LatticeGasSimPcb:

    def __init__(self,L,b,seed=12345678):
        """
        Inizializza tutte le variabili globali utilizzate, genera le regole di collisione, inizializza il reticolo con
        la densità desiderata e con l'ostacolo desiderato.

        Args:
        L - Dimensione del reticolo L*L
        b - Dimensioni del quadrato di particelle iniziale
        seed - seed per la generazione di numeri casuali
        """
    
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
        self.Lx = L
        self.Ly = L
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
        Lhalf = int((L-1)/2)
        self.lattice[int(Lhalf-b/2):int(Lhalf+b/2),int(Lhalf-b/2):int(Lhalf+b/2)] = 127


        self.avex = []
        self.avey = []
        self.havex = []
        self.havey = []
        

    
    def draw_colors(self):
        """
        Tramite la funzione count_lattice() genera un array per colorare il reticolo, barr è il colore della barriera 
        e parr quello delle particelle, entrambi in formato RGB.
        """

        barr = np.array([1.,0.,0.])
        parr = np.array([0.,0.,1.])
        return gl.count_lattice(barr,parr,self.lattice)


    
    def simulation(self,n):
        """
        Funzione chiamata per progredire con la simulazione.

        Args:
        n - indica il numero di step che si desidera simulare
        """

        for i in range(n):
            self.lattice = gl.update_lattice_pcb(self.lattice).astype(dtype=np.uint8,order='F')


    def test(self):
        avx = 0
        avy = 0
        hvex = []
        hvey = []
        for i in range(self.Lx):
            for j in range(self.Lx):
                if self.lattice[i,j] != 0:
                    avx += i
                    avy += j
                    hvex.append(i)
                    hvey.append(j)
        self.havex.append(hvex)
        self.havey.append(hvey)
        self.avex.append(avx/self.N)
        self.avey.append(avy/self.N)


    
    def animation1(self,frames,dpf=30,dpi=80,filename="Sim",format="gif",fps=10):
        """
        Funzione che genera un'animazione della simulazione. Questa visualizza le velocità tramite vettori
        calcolati tramite coarse grained average.
        
        Args:
        frames - il numero di frame da disegnare
        dpf - il numero di step della simulazione per ogni frame
        dpi - dpi dell'immagine se si sceglie il formato gif
        filename - nome del file di output dell'animazione
        formato - formato del file di output (gif o mp4)
        """

        # Funzione che genera i frame dell'animazione
        def update(frame): 
            
            # Calcolo dei colori
            colors = self.draw_colors() 

            self.test()

            # Avanzamento della simualzione
            self.simulation(dpf)

            # Aggiornamento del titolo
            axs.set_title("time step "+str(frame*dpf))

            p_bar.update()
            if frame==frames-1:
                tqdm.close(p_bar)
                print("Salvataggio...")  

            # Aggiornamento dei colori del reticolo                  
            return collection.set_facecolors(colors)

        # Parameters
        x_dim = self.Lx
        y_dim = self.Ly
        diam = 1
        
        # Generazione dell'animazione
        figure, axs = plt.subplots()
        axs.set_xlabel("x")
        axs.set_ylabel("y")
        
        # Generazione degli esagoni
        print("Inizializzazione...")        
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
        
        # Salvataggio
        if format == "gif":
            ani.save(filename="Examples/"+filename+".gif", writer="pillow",dpi=dpi,fps=fps)
        elif format == "mp4":
            Writer = animation.writers['ffmpeg']
            writer = Writer(fps=20, metadata=dict(artist='Me'), bitrate=8000)
            ani.save(filename="Examples/"+filename+".mp4", writer=writer)
