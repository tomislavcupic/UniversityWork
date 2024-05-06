import Bio
import numpy as np
from Bio.SeqIO import parse
from google.colab import drive
try:
  import google.colab
except ImportError:
    pass
drive.mount('/content/drive')
import os
print(os.getcwd())
os.chdir("drive/My Drive/Colab Notebooks/Obrada informacija/Lab2")

def assign_number(letter):
  number = 0
  letter = letter.upper()
  if letter == "A":
    number = 3
  elif letter == "G":
    number = 2
  elif letter == "C":
    number = -2
  elif letter == "T":
    number = -3
  return number
#
genome_list = list(parse("escherichia_coli_reference.fasta", "fasta"))
readings_list = list(parse("ecoli_ILL_small.fastq", "fastq"))
print(len(genome_list))
print(len(readings_list))
#
print(f"identifikator prvog očitanja {readings_list[0].id}")
reading_sequence = readings_list[0].seq
print(f"sekvenca prvog očitanja je {reading_sequence}")
print(f"identifikator E.coli {genome_list[0].id}")
reference_genome= genome_list[0].seq[:200:]
print(f"prvih 200 znakova za referentni E.coli je {reference_genome}")
#
nuc2num = ['A', 'G', 'C', 'T', 'N']
values = [assign_number(i) for i in nuc2num]
avg = np.average(values)
std = np.std(values)

x1 = [assign_number(i) for i in genome_list[0].seq]
x2 = [assign_number(i) for i in reading_sequence]
k_arr = range(-len(x2)+1,len(x1))
x1 = [(x-avg)/std for x in x1]
x2 = [(x-avg)/std for x in x2]
padding1 = [0]*(len(x2)-1)
padding2 = [0]*(len(x1)-1)
X1 = np.fft.fft(padding1 + x1)
X2 = np.fft.fft(x2 + padding2)
Cor = np.conjugate(X2)*X1
cor = np.fft.ifft(Cor)

k1 = k_arr[cor.argmax()]
print(f"Correlation by FFT: {np.real(cor)}")
print("k={}".format(k1))
#
print(len(genome_list[0].seq))
avg_list = []
for i in range(len(readings_list)):
  avg_list.append(len(readings_list[i].seq))
print(np.average(avg_list))
print(np.std(avg_list))
#
nuc2num = ['A', 'G', 'C', 'T', 'N']
values = [assign_number(i) for i in nuc2num]
avg = np.average(values)
std = np.std(values)
x1 = [assign_number(i) for i in genome_list[0].seq]
x1 = [(x-avg)/std for x in x1]
padding1 = [0] * (len(readings_list[0].seq) - 1)
padding2 = [0]*(len(x1)-1)
X1 = np.fft.fft(padding1+x1)

for i in range(10):

  sequence = readings_list[i].seq
  x2 = [assign_number(i) for i in sequence]
  x2 = [(x-avg)/std for x in x2]
  X2 = np.fft.fft(x2 + padding2)
  #print(len(X2))
  #print(len(X1))
  Cor = np.conjugate(X2)*X1
  cor = np.fft.ifft(Cor)
  k = k_arr[cor.argmax()]
  print(f"Correlation by FFT: {np.real(cor)}")
  print("k={}".format(k))
#

def Hamming_distance(sequence1, sequence2):
  distance = 0
  for i in range(0,len(sequence1)):
    if sequence2[i] != sequence1[i]:
      distance += 1
  return distance

part_ref = genome_list[0].seq[k1:k1+len(readings_list[0].seq)]
print(f"razlika u Hammingovoj distanci je {Hamming_distance(part_ref, readings_list[0].seq)}")
#
import csv
tsv_file = open("ecoli_ILL_small_aln.sam")
tsv_rows = csv.reader(tsv_file, delimiter="\t")
tsv_list_rows = list(tsv_rows)
for i in tsv_list_rows:
  if i[0] == readings_list[0].id:
    print(f"vrijednost u SAM datoteci je {i[3]}")
print(f"korelacijom sam dobio {k1}")
#
nuc2num = ['A', 'G', 'C', 'T', 'N']
values = [assign_number(i) for i in nuc2num]
avg = np.average(values)
std = np.std(values)
x1 = [assign_number(i) for i in genome_list[0].seq]
x1 = [(x-avg)/std for x in x1]
padding1 = [0] * (len(readings_list[0].seq) - 1)
padding2 = [0]*(len(x1)-1)
X1 = np.fft.fft(padding1+x1)
number_of_readings = 0
for i in range(100):
  sequence = readings_list[i].seq
  x2 = [assign_number(i) for i in sequence]
  x2 = [(x-avg)/std for x in x2]
  X2 = np.fft.fft(x2 + padding2)
  Cor = np.conjugate(X2)*X1
  cor = np.fft.ifft(Cor)
  k = k_arr[cor.argmax()]
  for row in tsv_list_rows:
    if row[0] == readings_list[i].id:
      if abs(int(row[3]) - k) <= 5:
        number_of_readings+=1

print(f"Broj očitanja za koja se dvije pozicije razlikuju za najviše 5 mjesta je {number_of_readings}")
#
