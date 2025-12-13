import time
import datetime
import statistics
import os

class SlijedBrojeva:
   def __init__(self, izvor_brojeva):
      self.izvor_brojeva = izvor_brojeva
      self.kolekcija = []
      self.akcije = {}

   def dodaj_akciju(self, key, akcija):
      self.akcije[key] = akcija

   def ukloni_akciju(self, key):
      del self.akcije[key]

   def obavijesti_akciju(self):
      for akcija in self.akcije.values():
         akcija.obavijesti(self)

   def kreni(self):
      while not self.izvor_brojeva.iscrpljeni_izvor():
         broj = self.izvor_brojeva.dohvati_broj()
         print(broj)
         if broj == -1:   
            break
         self.kolekcija.append(broj)
         self.obavijesti_akciju()
         time.sleep(1)
      print()

class IzvorBrojeva:
   def dohvati_broj(self):
      pass
   def iscrpljeni_izvor(self):
      pass

class TipkovnickiIzvor(IzvorBrojeva):
   def dohvati_broj(self):
      try:
         return int(input("Unesite broj: "))
      except ValueError:
         print("Neispravan unos, probajte ponovno.")
         return self.dohvati_broj()
   def iscrpljeni_izvor(self):
      return False

class DatotecniIzvor(IzvorBrojeva):
   def __init__(self, datoteka):
      self.datoteka = datoteka

   def dohvati_broj(self):
      return int(self.datoteka.readline().strip())
   def iscrpljeni_izvor(self):
      return self.datoteka.tell() == os.fstat(self.datoteka.fileno()).st_size

class Akcija:
   def obavijesti(self, subjekt):
      pass

class ZapisUDatotekuAkcija(Akcija):
   def obavijesti(self, subjekt):
      with open("kolekcija.txt", "a") as f:
         f.write(f"{subjekt.kolekcija} - {datetime.datetime.now()}\n")

class SumaAkcija(Akcija):
   def obavijesti(self, subjekt):
      print("Suma elemenata:", sum(subjekt.kolekcija))

class ProsjekAkcija(Akcija):
   def obavijesti(self, subjekt):
      print("Prosjek elemenata:", statistics.mean(subjekt.kolekcija))

class MedijanAkcija(Akcija):
   def obavijesti(self, subjekt):
      print("Medijan elemenata:", statistics.median(subjekt.kolekcija))

def main():
   tipkovnicki_izvor = TipkovnickiIzvor()
   datotecni_izvor = DatotecniIzvor(open("peti.txt"))
   slijed_brojeva_datoteka = SlijedBrojeva(datotecni_izvor)
   slijed_brojeva = SlijedBrojeva(tipkovnicki_izvor)

   slijed_brojeva.dodaj_akciju("zapis_u_datoteku", ZapisUDatotekuAkcija())
   slijed_brojeva.dodaj_akciju("suma" ,SumaAkcija())
   slijed_brojeva.dodaj_akciju("prosjek", ProsjekAkcija())
   slijed_brojeva.dodaj_akciju("medijan", MedijanAkcija())
   slijed_brojeva.dodaj_akciju("zapis", ZapisUDatotekuAkcija())
   slijed_brojeva.ukloni_akciju("zapis")

   slijed_brojeva_datoteka.dodaj_akciju("zapis", ZapisUDatotekuAkcija())
   slijed_brojeva_datoteka.dodaj_akciju("suma", SumaAkcija())
   slijed_brojeva_datoteka.dodaj_akciju("prosjek", ProsjekAkcija())
   slijed_brojeva_datoteka.dodaj_akciju("medijan", MedijanAkcija())

   slijed_brojeva_datoteka.kreni()
   slijed_brojeva.kreni()

if __name__ == "__main__":
   main()