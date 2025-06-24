import argparse
from queue import Queue, PriorityQueue

def main():
   parser = argparse.ArgumentParser(description='Ispisuje sadržaj datoteke.')
   parser.add_argument('--alg', help='Algoritam za pretraživanje', choices=['bfs', 'ucs', 'astar'], required=False)
   parser.add_argument('--ss', help='putanja do opisnika prostora stanja', required=True)
   parser.add_argument('--h', help='putanja do heuristike', required=False)
   parser.add_argument('--check-optimistic', help='provjera optimističnosti', action='store_true', required=False)
   parser.add_argument('--check-consistent', help='provjera konzistentnosti', action='store_true', required=False)

   args = parser.parse_args()

   algorithm = args.alg
   filename = args.ss
   heuristic = args.h
   check_optimistic = args.check_optimistic
   check_consistent = args.check_consistent

   with open(filename, 'r', encoding='utf-8') as file:
      if algorithm == 'bfs':
         bfs(file)
      elif algorithm == 'ucs':
         ucs(file)
      elif algorithm == 'astar':
         astar(file, heuristic, check_optimistic, check_consistent)
    #   if check_optimistic:
    #      optimistic3(file, heuristic)
    #   if check_consistent:
    #      consistent(file, heuristic) 
 
def astar(file, heuristic, check_optimistic, check_consistent):
    # micemo komentare iz prvih redova
    nadeno_rjesenje = False
    broj_posjecenih = 0
    putanja = []
    cijena = 0.0
    funkcija = 0.0
    while True:
        line = file.readline()
        if line.startswith('#'):
            continue
        else:
            pocetno_stanje = line.strip()
            putanja.append(pocetno_stanje)
            break
    heuristika = {}
    for line in open(heuristic, "r", encoding='utf-8'):
        if line.startswith('#'):
            continue
        heuristika[line.split()[0].strip(":")] = float(line.split()[1])
    #print(heuristika)
    zavrsna_stanja = file.readline().strip().split(" ")
    posjeceni_cvorovi = set()
    posjeceni_cvorovi.add(pocetno_stanje)
    red = PriorityQueue()
    red.put((funkcija, cijena,pocetno_stanje, putanja))
    #print("red", red.queue)
    svi_cvorovi = {}
    for line in file:
        if line.startswith('#'):
            continue
        svi_cvorovi[line.split()[0].strip(":")] = sorted(line.split()[1:])
    
    # mapa za pracenje cijena cvorova
    cijene_cvorova = {pocetno_stanje: 0}
   
    while not red.empty():

        funkcija, trenutna_cijena, trenutna_stanje, trenutna_putanja = red.get()
       
        broj_posjecenih += 1
        
        if trenutna_stanje in zavrsna_stanja:
            nadeno_rjesenje = True
            putanja = trenutna_putanja
            cijena = trenutna_cijena
            break
        
        for sljedeci in svi_cvorovi[trenutna_stanje]:
            sljedeci_stanje, sljedeca_cijena = sljedeci.split(",")
            sljedeca_cijena = float(sljedeca_cijena)
            nova_cijena = trenutna_cijena + sljedeca_cijena
            funkcija = nova_cijena + heuristika[sljedeci_stanje]
            if sljedeci_stanje not in cijene_cvorova or nova_cijena < cijene_cvorova[sljedeci_stanje]:
                cijene_cvorova[sljedeci_stanje] = nova_cijena
                red.put((funkcija, nova_cijena, sljedeci_stanje, trenutna_putanja + [sljedeci_stanje]))
                posjeceni_cvorovi.add(sljedeci_stanje)
   
    if nadeno_rjesenje:
        print("# A-STAR", heuristic)
        printanje(broj_posjecenih, putanja, cijena)
    else:
        print("[FOUND_SOLUTION]: no")

def bfs(file):
   # micemo komentare iz prvih redova
   nadeno_rjesenje = False
   broj_posjecenih = 0
   putanja = []
   cijena = 0.0
   while True:
      line = file.readline()
      if line.startswith('#'):
         continue
      else:
         pocetno_stanje = line.strip()
         putanja.append(pocetno_stanje)
         break
   zavrsna_stanja = file.readline().strip().split(" ")
   posjeceni_cvorovi = set()
   posjeceni_cvorovi.add(pocetno_stanje)
   red = Queue()
   red.put((pocetno_stanje, putanja, cijena))
   svi_cvorovi = {}
   for line in file:
      if line.startswith('#'):
         continue
      svi_cvorovi[line.split()[0].strip(":")] = sorted(line.split()[1:])

   while not red.empty():
      trenutno_stanje, trenutna_putanja, trenutna_cijena = red.get()
      trenutno_stanje = trenutno_stanje.split(",")[0]
      broj_posjecenih = broj_posjecenih + 1
      if trenutno_stanje in zavrsna_stanja:
         nadeno_rjesenje = True
         putanja = trenutna_putanja
         cijena = trenutna_cijena
         break
      for sljedeci in svi_cvorovi[trenutno_stanje]:
         if sljedeci.split(",")[0] not in posjeceni_cvorovi:
            red.put((sljedeci, trenutna_putanja + [sljedeci.split(",")[0]], trenutna_cijena + float(sljedeci.split(",")[1])))
            posjeceni_cvorovi.add(sljedeci.split(",")[0])

   if nadeno_rjesenje:
    print("# BFS")
    printanje(broj_posjecenih, putanja, cijena)
   else:
    print("[FOUND_SOLUTION]: no")

def ucs(file):
    # micemo komentare iz prvih redova
    nadeno_rjesenje = False
    broj_posjecenih = 0
    putanja = []
    cijena = 0.0
    
    while True:
        line = file.readline()
        if line.startswith('#'):
            continue
        else:
            pocetno_stanje = line.strip()
            putanja.append(pocetno_stanje)
            break
    
    zavrsna_stanja = set(file.readline().strip().split(" "))
    posjeceni_cvorovi = set()
    posjeceni_cvorovi.add(pocetno_stanje)

    red = PriorityQueue()
    red.put((cijena, pocetno_stanje, putanja)) 
    
    svi_cvorovi = {}
    for line in file:
        if line.startswith('#'):
            continue
        svi_cvorovi[line.split()[0].strip(":")] = sorted(line.split()[1:])
    
    cijene_cvorova = {pocetno_stanje: 0}
   
    while not red.empty():
        trenutna_cijena, trenutna_stanje, trenutna_putanja = red.get()
        trenutna_stanje = trenutna_stanje.split(",")[0]
        broj_posjecenih += 1
        
        if trenutna_stanje in zavrsna_stanja:
            nadeno_rjesenje = True
            putanja = trenutna_putanja
            cijena = trenutna_cijena
            break
        
        for sljedeci in svi_cvorovi[trenutna_stanje]:
            sljedeci_stanje, sljedeca_cijena = sljedeci.split(",")
            sljedeca_cijena = float(sljedeca_cijena)
            nova_cijena = trenutna_cijena + sljedeca_cijena
            if sljedeci_stanje not in cijene_cvorova or nova_cijena < cijene_cvorova[sljedeci_stanje]:
                cijene_cvorova[sljedeci_stanje] = nova_cijena
                red.put((nova_cijena, sljedeci_stanje, trenutna_putanja + [sljedeci_stanje]))
                posjeceni_cvorovi.add(sljedeci_stanje)
   
    if nadeno_rjesenje:
        print("# UCS")
        printanje(broj_posjecenih, putanja, cijena)
    else:
        print("[FOUND SOLUTION]: no")

def printanje(broj_posjecenih, putanja, cijena):
    print("FOUND_SOLUTION: yes")
    print("[STATES_VISITED]:", broj_posjecenih)
    print("[PATH_LENGTH]:", len(putanja))
    print("[TOTAL_COST]:", round(cijena, 1))
    print("[PATH]:"," => ".join(putanja))

if __name__ == '__main__':
   main()