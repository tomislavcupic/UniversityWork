from mpi4py import MPI
import random
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

LIJEVI = (rank - 1 + size) % size
DESNI = (rank + 1) % size

#vilic(ima vilicu, je cista)
if rank == 0:
   vilice = {
      LIJEVI: (True, False),
      DESNI: (True, False)
   }
else:
   vilice = {
      LIJEVI: (rank < LIJEVI, False),
      DESNI: (rank < DESNI, False)
   }

zahtjevi = {LIJEVI: False, DESNI: False}

MISLIM = 0
GLADAN = 1
JEDEM = 2
stanje = MISLIM

def log(msg):
   print(f"[{rank}]: {msg}", flush=True)

def posalji_vilicu(susjed):
   global vilice
   vilice[susjed] = (False, True)
   comm.send(('VILICA', rank, True), dest=susjed)
   #log(f"ocistio vilicu")
   if size == 2:
      log(f"poslao vilice {susjed}")
   else:
      log(f"poslao vilicu {susjed}")

def obradi_poruke():
   global vilice, zahtjevi
   status = MPI.Status()
   while comm.Iprobe(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status):
      src = status.Get_source()
      poruka = comm.recv(source=src)
      #print(f"primio poruku {poruka} od {src}")
      tip = poruka[0]

      if tip == 'ZAHTJEV':
         trazioc = poruka[1]
         if stanje != JEDEM and stanje != GLADAN and vilice[trazioc][0] and not vilice[trazioc][1]:
            posalji_vilicu(trazioc)
         else:
            zahtjevi[trazioc] = True

      elif tip == 'VILICA':
         posiljatelj, je_cista = poruka[1], poruka[2]
         vilice[posiljatelj] = (True, je_cista)
         if size == 2:
            log(f"dobio vilice od {posiljatelj}")
         else:
            log(f"dobio vilicu od {posiljatelj}")

      else:
         log(f"nepoznata poruka {tip} od {src}")

def odgovori_na_zahtjeve():
   global zahtjevi
   for susjed in [LIJEVI, DESNI]:
      if zahtjevi[susjed] and vilice[susjed][0] and not vilice[susjed][1]:
         posalji_vilicu(susjed)
         zahtjevi[susjed] = False

def filozof():
   global stanje, vilice

   while True:
      stanje = MISLIM
      log("mislim, dakle postojim")
      t_end = time.time() + random.randint(1, 5)
      while time.time() < t_end:
         obradi_poruke()
         time.sleep(0.5)

      stanje = GLADAN
      log("gladan")

      for susjed in [LIJEVI, DESNI]:
         if not vilice[susjed][0]:
            log(f"trazim vilicu od {susjed}")
            comm.send(('ZAHTJEV', rank), dest=susjed)

      while not (vilice[LIJEVI][0] and vilice[DESNI][0]):
         obradi_poruke()
         time.sleep(0.1)

      stanje = JEDEM
      log("jedem")
      time.sleep(random.randint(1, 4))
      vilice[LIJEVI] = (True, False)
      vilice[DESNI] = (True, False)

      odgovori_na_zahtjeve()
      
filozof()