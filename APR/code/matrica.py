class Matrica:
   epsilon = 1e-8

   def __init__(self,rows=0,columns=0, data=None) -> None:
      if data is None:
         self.data = [[0.0 for _ in range(columns)] for _ in range(rows)] 
         self.rows = rows
         self.columns = columns
      else:
         self.data = data
         self.rows = len(data)
         self.columns = len(data[0]) if data else 0
   
   def check_square(self) -> None:
      if self.columns != self.rows:
         raise ValueError("matrica mora biti kvadratna!")

   def __getitem__(self, index) -> list:
      return self.data[index]

   def __setitem__(self, index, value) -> None:
      self.data[index] = value

   def set_element(self, i, j, value) -> None:
      self.data[i][j] = value

   def get_element(self, i, j) -> float:
      return self.data[i][j]

   @staticmethod
   def read_from_file(file) -> 'Matrica':
      with open(file, 'r') as f:
         lines = f.readlines()
         matrix = []
         for line in lines:
            matrix.append([float(x) for x in line.split()])
         return Matrica(data=matrix)

   def write_to_file(self, file) -> None:
      with open(file, 'a') as f:
         for row in self.data:
            a = [str(x) for x in row]
            f.write(" ".join(a))
            f.write("\n")

   def __eq__(self, matrix2) -> bool:
      for i in range(len(self.data)):
         for j in range(len(self.data[i])):
            if matrix2.data[i][j] != self.data[i][j]:
               return False
      return True
   
   def __add__(self, matrix2) -> 'Matrica':
      if not isinstance(matrix2, Matrica):
         result = Matrica(self.rows, self.columns)
         for i in range(len(self.data)):
            for j in range(len(self.data[i])):
               result[i][j] = self.data[i][j] + matrix2
         return result
      if self.columns != matrix2.columns or self.rows != matrix2.rows:
         raise ValueError("matrice nemaju isti broj redova i stupaca")
      result = Matrica(self.rows, self.columns)
      for i in range(len(self.data)):
         for j in range(len(self.data[i])):
            result[i][j] = matrix2.data[i][j] + self.data[i][j]
      return result

   def __sub__(self, matrix2) -> 'Matrica':
      if isinstance(matrix2, Matrica):
         if self.columns != matrix2.columns or self.rows != matrix2.rows:
            raise ValueError("matrice nemaju isti broj redova i stupaca")
         result = Matrica(self.rows, self.columns)
         for i in range(len(self.data)):
            for j in range(len(self.data[i])):
               result[i][j] = matrix2.data[i][j] - self.data[i][j]
         return result
      else:
         result = Matrica(self.rows, self.columns)
         for i in range(len(self.data)):
            for j in range(len(self.data[i])):
               result[i][j] = self.data[i][j] - matrix2
         return result

   def __iadd__(self, matrix2) -> 'Matrica':
      if self.columns != matrix2.columns or self.rows != matrix2.rows:
         raise ValueError("matrice nemaju isti broj redova i stupaca")
      for i in range(len(self.data)):
         for j in range(len(self.data[i])):
            self.data[i][j] += self.data[i][j]
      return self

   def __isub__(self, matrix2) -> 'Matrica':
      if self.columns != matrix2.columns or self.rows != matrix2.rows:
         raise ValueError("matrice nemaju isti broj redova i stupaca")
      for i in range(len(self.data)):
         for j in range(len(self.data[i])):
            matrix2.data[i][j] -= self.data[i][j]
      return self

   def __str__(self) -> str:
      str_matrix = ""
      for row in self.data:
         a = [str(x) for x in row]
         str_matrix += (" ".join(a))
         str_matrix += "\n"
      return str_matrix
   
   def __mul__(self, second) -> 'Matrica':
      if isinstance(second, Matrica):
         if self.columns != second.rows:
            raise ValueError("matrice nisu kompatibilne za množenje")
         result = Matrica(self.rows, second.columns)
         for i in range(self.rows):
            for j in range(second.columns):
               result[i][j] = sum(self.data[i][k] * second.data[k][j] for k in range(self.columns))
      else:
         result = Matrica(self.rows, self.columns)
         for i in range(len(self.data)):
            for j in range(len(self.data[i])):
               result[i][j] = self.data[i][j] * second
      return result

   def __rmul__(self, second) -> 'Matrica':
      return  self.__mul__(second)
   
   def __radd__(self, second) -> 'Matrica':
      return self.__add__(second)

   def __rsub__(self, second) -> 'Matrica':
      return self.__sub__(second)

   def T(self) -> 'Matrica':
      result = Matrica(self.columns, self.rows)
      for i in range(len(self.data)):
         for j in range(len(self.data[i])):
            result[j][i] = self.data[i][j]
      return result

   def supstitution_forward(self, vector) -> 'Matrica':
      self.check_square()
      oldvector = vector
      for i in range(0, self.rows - 1):
         if abs(self.data[i][i]) < self.epsilon:
            print("dijeljenje s nulom u supstituciji unaprijed")
            return oldvector
         for j in range(i + 1, self.rows):
            num = self.data[j][i]
            if i == j:
               num = 1
            vector[j][0] -= num * vector[i][0]
      return vector
   
   def supstitution_backward(self, vector) -> 'Matrica':
      self.check_square()
      oldvector = vector
      for i in range(self.rows -1, -1, -1):
         if abs(self.data[i][i]) < self.epsilon:
            print("dijeljenje s nulom u supstituciji unatrag")
            return None
         vector[i][0] = vector[i][0] / self.data[i][i]
         for j in range(0, i):
            vector[j][0] -= self.data[j][i] * vector[i][0]
      return vector
   
   def LU_decomposition(self) -> 'Matrica':
      self.check_square()
      oldself = self
      try:
         for i in range(0, self.rows-1):
            for j in range(i+1, self.rows):
               if abs(self.data[i][i]) < self.epsilon:
                  print("dijeljenje s nulom u LU dekompoziciji")
                  return oldself
               self.data[j][i] /= self.data[i][i]
               for k in range(i+1, self.rows):
                  self.data[j][k] -= self.data[j][i] * self.data[i][k]
      except ValueError:
         print("ne moze se izracunati LU dekompozicija")
         return oldself
      return self
      
   def LUP_decomposition(self) -> 'Matrica':
      self.check_square()
      oldself = self
      num_permutations = 0
      P2 = [i for i in range(self.rows)]
      P = Matrica(1, self.rows, [P2])
      for i in range(self.rows):
         pivot = i
         for j in range(i + 1, self.rows):
            if abs(self.data[j][i]) > abs(self.data[pivot][i]):
               pivot = j
         if pivot != i:
            self.data[i], self.data[pivot] = self.data[pivot], self.data[i]
            P[0][i], P[0][pivot] = P[0][pivot], P[0][i]
            num_permutations += 1
         for j in range(i + 1, self.rows):
            if abs(self.data[i][i]) < self.epsilon:
               print("dijeljenje s nulom u LUP dekompoziciji")
               return oldself, P, num_permutations
            self.data[j][i] /= self.data[i][i]
            for k in range(i + 1, self.columns):
               self.data[j][k] -= self.data[j][i] * self.data[i][k]
      return self, P, num_permutations

   # funkcija za izračun inverza matrice operatorom ~
   def __invert__(self) -> 'Matrica':
      self.check_square()
      LU, P, _ = self.LUP_decomposition()
      inverse = Matrica(self.rows, self.columns)
      for i in range(self.rows):
         vector = Matrica(self.rows, 1)
         vector[i][0] = 1
         vector = vector.apply_permutation_to_vector(P)
         vector = LU.supstitution_forward(vector)
         vector = LU.supstitution_backward(vector)
         if vector is None:
            print("ne moze se izracunati inverz")
            return None
         for j in range(self.rows):
            inverse[j][i] = vector[j][0]
      return inverse

   def determinant(self) -> float:
      self.check_square()
      LU, P, num = self.LUP_decomposition()
      det = 1
      for i in range(self.rows):
         det *= LU.data[i][i]
      return det * (-1)**num

   def apply_permutation_to_vector(self, P) -> 'Matrica':
      permuted_vector = Matrica(self.rows, 1)
      for i in range(P.T().len()):
         permuted_vector[i][0] = self.data[P[0][i]][0]
      return permuted_vector
   
   def norm(self) -> 'float':
      return sum(sum(abs(x) for x in row) for row in self.data)
   
   def len(self):
      return self.rows
   
   def tolist(self) -> 'list':
      lista = []
      for i in range(self.rows):
         for j in range(self.columns):
            lista.append(self.data[i][j])
      return lista
   
   def identity(self, rows=None) -> 'Matrica':
      if not rows:
         I = Matrica(self.rows, self.rows)
      else:
         I = Matrica(rows, rows)
      for i in range(self.rows):
         I[i][i] = 1
      return I
   
   def power(self, x) -> None:
      for i in range(self.rows):
         for j in range(self.columns):
            self.data[i][j] = self.data[i][j] ** x

   def solve(self, vector) -> 'Matrica':
      self, P, num_permutations = self.LUP_decomposition()
      vector = vector.apply_permutation_to_vector(P)
      vector = self.supstitution_forward(vector)
      vector = self.supstitution_backward(vector)
      return vector