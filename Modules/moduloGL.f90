module moduloGL

    implicit none
    public :: gen_rules, update_lattice, count_lattice, vel_lattice, update_lattice_pcb
    integer(kind=2) :: RI,RD,LD,LE,LU,RU,S,B                                                ! Definizione delle velocità
    integer :: NUM_RULES,numParticles
    integer(kind=2), dimension(:),allocatable :: rule                                       ! Array con le regole di collisione
    real :: vxTotal,vyTotal,flowRate,scale
    real, dimension(:), allocatable :: vx,vy                                                ! Array delle possibili velocità per ogni combinazione di velocità
    real, dimension(0:6) :: ux,uy                                                           ! Velocità per ogni direzione

    contains


    ! Questa funzione gestisce l'inizializzazione di tutte le variabili utilizzate, oltre che 
    ! generare le regole di collisione e le velocità possibili per un dato sito 
    subroutine gen_rules(N,fr,sc,seed)
        integer(kind=2) :: i,tmp,lowBits,highBits,j
        integer, dimension(8) :: seed
        integer :: N
        real :: fr,sc
        
        ! Passo il seed da pyhton
        call random_seed( put = seed )

        ! Inizializzazione di tutte le variabili utilizzate
        numParticles = N
        flowRate = fr
        scale = sc

        NUM_RULES = ISHFT(1,8)

        RI = 1      
        RD = 2
        LD = 4
        LE = 8
        LU = 16
        RU = 32        
        S = 64
        B = 128
        ux = [1.0, 0.5, -0.5, -1.0, -0.5, 0.5, 0.]
        uy = [0.0, -sqrt(3.)/2., -sqrt(3.)/2., 0.0, sqrt(3.)/2., sqrt(3.)/2., 0.]
        
        ! Allocazione dei vettori in caso questi non siano già allocati (per evitare crash nel kernel)
        if ( .not. allocated(rule) ) then
            allocate(rule(0:NUM_RULES-1))
            allocate(vx(0:NUM_RULES-1))
            allocate(vy(0:NUM_RULES-1))
        end if        


        ! Generazione di tutte le regole di collisione
        rule = 0

        do i = 0, B-1
            rule(i) = i
        end do
        rule(ior(ior(LU,LD),RI)) = ior(ior(RU,LE),RD)
        rule(ior(ior(RU,LE),RD)) = ior(ior(LU,LD),RI)
        rule(ior(ior(RU,LU),LD)) = ior(ior(LU,LE),RI)
        rule(ior(ior(LU,LE),RI)) = ior(ior(RU,LU),LD)
        rule(ior(ior(RU,LU),RD)) = ior(ior(RU,LE),RI)
        rule(ior(ior(RU,LE),RI)) = ior(ior(RU,LU),RD)
        rule(ior(ior(RU,LD),RD)) = ior(ior(LE,RD),RI)
        rule(ior(ior(LE,RD),RI)) = ior(ior(RU,LD),RD)
        rule(ior(ior(LU,LD),RD)) = ior(ior(LE,LD),RI)
        rule(ior(ior(LE,LD),RI)) = ior(ior(LU,LD),RD)
        rule(ior(ior(RU,LD),RI)) = ior(ior(LU,RD),RI)
        rule(ior(ior(LU,RD),RI)) = ior(ior(RU,LD),RI)
        rule(ior(ior(LU,LE),RD)) = ior(ior(RU,LE),LD)
        rule(ior(ior(RU,LE),LD)) = ior(ior(LU,LE),RD)
        rule(ior(LE,RI)) = ior(RU,LD)
        rule(ior(RU,LD)) = ior(LU,RD)
        rule(ior(LU,RD)) = ior(LE,RI)
        rule(ior(ior(ior(RU,LU),LD),RD)) = ior(ior(ior(RU,LE),LD),RI)
        rule(ior(ior(ior(RU,LE),LD),RI)) = ior(ior(ior(LU,LE),RD),RI)
        rule(ior(ior(ior(LU,LE),RD),RI)) = ior(ior(ior(RU,LU),LD),RD)
        rule(ior(LU,RI)) = ior(RU,S)
        rule(ior(RU,LE)) = ior(LU,S)
        rule(ior(LU,LD)) = ior(LE,S)
        rule(ior(LE,RD)) = ior(LD,S)
        rule(ior(LD,RI)) = ior(RD,S)
        rule(ior(RD,RU)) = ior(RI,S)
        rule(ior(ior(ior(ior(LU,LE),LD),RD),RI)) = ior(ior(ior(ior(RU,LE),LD),RD),S)
        rule(ior(ior(ior(ior(RU,LE),LD),RD),RI)) = ior(ior(ior(ior(LU,LD),RD),RI),S)
        rule(ior(ior(ior(ior(RU,LU),LD),RD),RI)) = ior(ior(ior(ior(RU,LE),RD),RI),S)
        rule(ior(ior(ior(ior(RU,LU),LE),RD),RI)) = ior(ior(ior(ior(RU,LU),LD),RI),S)
        rule(ior(ior(ior(ior(RU,LU),LE),LD),RI)) = ior(ior(ior(ior(RU,LU),LE),RD),S)
        rule(ior(ior(ior(ior(RU,LU),LE),LD),RD)) = ior(ior(ior(ior(LU,LE),LD),RI),S)
        do i = 0, int(S-1,kind=2)
            tmp = ior(ior(ior(ior(ior(ior(RU,LU),LE),LD),RD),RI),S)
            tmp = XOR(rule(i),tmp)
            rule(XOR(i,ior(ior(ior(ior(ior(ior( RU,LU),LE),LD),RD),RI),S))) = tmp
        end do 
        do i = B, int(NUM_RULES-1,kind=2)
            highBits = iand(i,(ior(ior(LE,LU),RU)))
            lowBits = iand(i,(ior(ior(RI,RD),LD)))
            rule(i) = ior(ior(B,ishft(highBits,-3)),ishft(lowBits,3))
        end do
        

        ! Generazione della tabella delle possibili velocità
        vx = 0
        vy = 0
        do i = 0, int(NUM_RULES-1,kind=2)
            do j = 0, 6                
                if (iand(i,ishft(int(1,kind=2),j))/=0 ) then
                    vx(i) = vx(i) + ux(j)
                    vy(i) = vy(i) + uy(j)
                end if                
            end do
        end do
        
    end subroutine gen_rules


    ! Questa funzione gestisce l'aggiornamento del reticolo, quindi l'aggioramento delle 
    ! velocità e infine è responsabile per garantire il flusso del liquido
    function update_lattice(lattice,Lx,Ly) result(newLattice)
        integer :: i,j,k,inj,Lx,Ly,tmp2
        integer(kind=2) :: site1,site2
        integer(kind=2), dimension(0:Ly-1,0:Lx-1) :: newLattice
        integer(kind=2), dimension(0:Ly-1,0:Lx-1) :: lattice
        integer  :: l,c,r
        real :: tmp

        
        newLattice = 0

        ! Aggiornamento delle posizioni delle particelle nel reticolo
        do i = 0, Lx-1                                                                              
            l = mod((i-1+Lx),Lx)
            c = i
            r = mod((i+1),Lx)
            

            do j = 1, Ly-3, 2
                site1 = lattice(j,i)
                site2 = lattice(j+1,i)


                newLattice(j-1,r) = ior(newLattice(j-1,r),iand(site1,RD))    
                newLattice(j-1,c) = ior(newLattice(j-1,c),iand(site1,LD))                
                newLattice(j,r) = ior(newLattice(j,r),iand(site1,RI))                 
                newLattice(j,c) = ior(newLattice(j,c),ior(iand(site1,ior(S,B)),iand(site2,RD)))                      
                newLattice(j,l) = ior(newLattice(j,l),ior(iand(site1,LE),iand(site2,LD)))                
                newLattice(j+1,r) = ior(newLattice(j+1,r),ior(iand(site1,RU),iand(site2,RI)))                
                newLattice(j+1,c) = ior(newLattice(j+1,c),ior(iand(site1,LU),iand(site2,ior(S,B))))                
                newLattice(j+1,l) = ior(newLattice(j+1,l),iand(site2,LE))                                                 
                newLattice(j+2,c) = ior(newLattice(j+2,c),iand(site2,RU))                                                  
                newLattice(j+2,l) = ior(newLattice(j+2,l),iand(site2,LU))
                
            end do 

        end do   

        ! Calcolo delle collisioni 
        vxTotal = 0
        vyTotal = 0
        do i = 0, Lx-1
            do j = 0, Ly-1
                site1 = rule(newLattice(j,i))
                newlattice(j,i) = site1
                vxTotal = vxTotal + vx(site1)
                vyTotal = vyTotal + vy(site1)
            end do
        end do


        ! Questo loop permette di ottenere il flusso di particelle 
        inj = int((flowRate*numParticles-vxTotal)/scale)            ! Numero di iniezioni per ottenere il flusso desiderato
        do k = 1, abs(inj) 
            call random_number(tmp)
            i = int(Lx*tmp)
            call random_number(tmp)
            j = int(Ly*tmp)
            
            if ( inj>0 ) then
                tmp2 = LE
            else
                tmp2 = RI
            end if

            if ((iand(newlattice(j,i),ior(RI,LE))) == tmp2) then
                newLattice(j,i) = xor(newLattice(j,i),ior(RI,LE))    ! Inverto RI e LE
            end if
        end do

    end function update_lattice


    ! Questa funzione è necessaria per contare quante particelle sono presenti in un sito 
    ! del reticolo e ritorna l'array di colori utilizzato in animation1() per colorare appropriatamente
    ! il reticolo
    function count_lattice(cP,cB,lattice,Lx,Ly) result(newLattice)
        integer :: i,j,Lx,Ly
        real :: bit
        real, dimension(0:Ly*Lx-1,3) :: newLattice
        real, dimension(3) :: cP,cB                     ! Array di colori in formato RGB passati in input
        integer, dimension(0:Ly-1,0:Lx-1) :: lattice

        ! Loop sul reticolo per il calcolo del numero di particelle
        do i = 0, Lx-1
            do j = 0, Ly-1
                bit = bit_count(lattice(j,i))
                if ( bit/=-1 ) then
                    newLattice(j*Lx+i,:) = cP*(1-exp(-bit/3))
                else
                    newLattice(j*Lx+i,:) = cB
                end if
                    
            end do
        end do
        
    end function count_lattice


    ! Semplice funzione che conta il numero di particelle in un dato sito del lattice o ritorna -1 se
    ! vi è presente una barriera
    function bit_count(n) result(count)
        integer :: i
        integer :: n
        integer :: count, bit

        count = 0

        i = 0

        do while (n /= 0)
            bit = mod(n, 2)            
            count = count + bit
            n = n / 2
            i = i + 1
        end do

        if ( bit == 1 .and. i>=8) then
            count = -1
        end if

    end function bit_count


    ! Funzione che calcola la coarse grained average velocity
    function vel_lattice(dx,dy,lattice,Lx,Ly) result(result)        
        integer :: Lx,Ly,dx,dy
        integer, dimension(0:Ly-1,0:Lx-1) :: lattice
        real, dimension(0:dy*2-1,0:dx-1) :: result
        integer :: i,j,k1,k2
        
        k1 = Lx/dx
        k2 = Ly/dy
        result = 0
        
        ! Loop sul reticolo in cui calcolo la somma delle velocità vx e vy su un quadrato k1*k2 
        do i = 0, Lx-mod(Lx,k1)-1
            do j = 0, Ly-mod(Ly,k2)-1
                result(j/k2,i/k1) = result(j/k2,i/k1) + vx(lattice(j,i))
                result(j/k2+dy,i/k1) = result(j/k2+dy,i/k1) + vy(lattice(j,i))
            end do
        end do
    end function vel_lattice


    ! Funzione molto simile a update_lattice() in cui sono presenti condizioni al contorno periodiche e 
    ! non vi è nessun flusso  
    function update_lattice_pcb(lattice,Lx,Ly) result(newLattice)
        integer :: i,j,Lx,Ly
        integer(kind=2) :: site1,site2
        integer(kind=2), dimension(0:Ly-1,0:Lx-1) :: newLattice
        integer(kind=2), dimension(0:Ly-1,0:Lx-1) :: lattice
        integer  :: l,c,r,u,uu,d

        
        newLattice = 0

        
        do i = 0, Lx-1
            l = mod((i-1+Lx),Lx)
            c = i
            r = mod((i+1),Lx)
            

            do j = 1, Ly-3, 2
                d = mod((j-1+Ly-2),Ly-2)
                u = mod((j+1),Ly-2)
                uu = mod((j+2),Ly-2)

                site1 = lattice(j,i)
                site2 = lattice(u,i)


                newLattice(d,r) = ior(newLattice(d,r),iand(site1,RD))    
                newLattice(d,c) = ior(newLattice(d,c),iand(site1,LD))                
                newLattice(j,r) = ior(newLattice(j,r),iand(site1,RI))                 
                newLattice(j,c) = ior(newLattice(j,c),ior(iand(site1,ior(S,B)),iand(site2,RD)))                      
                newLattice(j,l) = ior(newLattice(j,l),ior(iand(site1,LE),iand(site2,LD)))                
                newLattice(u,r) = ior(newLattice(u,r),ior(iand(site1,RU),iand(site2,RI)))                
                newLattice(u,c) = ior(newLattice(u,c),ior(iand(site1,LU),iand(site2,ior(S,B))))                
                newLattice(u,l) = ior(newLattice(u,l),iand(site2,LE))                                                 
                newLattice(uu,c) = ior(newLattice(uu,c),iand(site2,RU))                                                  
                newLattice(uu,l) = ior(newLattice(uu,l),iand(site2,LU))
                
            end do 

        end do   

        vxTotal = 0
        vyTotal = 0
        do i = 0, Lx-1
            do j = 0, Ly-1
                site1 = rule(newLattice(j,i))
                newlattice(j,i) = site1
                vxTotal = vxTotal + vx(site1)
                vyTotal = vyTotal + vy(site1)
            end do
        end do

    end function update_lattice_pcb

end module moduloGL