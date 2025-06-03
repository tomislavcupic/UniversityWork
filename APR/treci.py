from algoritmi import *
import matplotlib.pyplot as plt

def main():
   #sve funkcije:

   class PrvaFunkcija(CiljnaFunkcija):
      def f(self, x):
         self.broj_poziva_funkcije += 1
         return 100 * ((x[0][1] - x[0][0]**2)**2) + (1 - x[0][0])**2

      def grad_f(self, x):
         self.broj_poziva_gradijenta += 1
         return Matrica(1, 2, [[400 * (-1 * x[0][1] * x[0][0] + x[0][0]**3) - 2 + 2 * x[0][0], 200 * (x[0][1] - x[0][0]**2)]])

      def hess_f(self, x):
         self.broj_poziva_hesse += 1
         return Matrica(2, 2, [[1200 * x[0][0]**2 - 400*x[0][1] + 2, -400 * x[0][0]],[-400 * x[0][0], 200]])
   
   class DrugaFunkcija(CiljnaFunkcija):
      def f(self, x):
         self.broj_poziva_funkcije += 1
         return (x[0][0] - 4)**2 + 4*((x[0][1] - 2)**2)

      def grad_f(self, x):
         self.broj_poziva_gradijenta += 1
         return Matrica(1, 2, [[2 * (x[0][0] - 4) , 8 * (x[0][1] - 2)]])

      def hess_f(self, x):
         self.broj_poziva_hesse += 1
         return Matrica(2, 2, [[2, 0], [0, 8]])
      
   class TrecaFunkcija(CiljnaFunkcija):
      def f(self, x):
         self.broj_poziva_funkcije += 1
         return (x[0][0] - 2)**2 + (x[0][1] + 3)**2
   
      def grad_f(self, x):
         self.broj_poziva_gradijenta += 1
         return Matrica(1, 2, [[2 * (x[0][0] - 2), 2 * (x[0][1] + 3)]])

      def hess_f(self, x):
         self.broj_poziva_hesse += 1
         return Matrica(2, 2, [[2, 0],[0, 2]])
      
   class CetvrtaFunkcija(CiljnaFunkcija):
      def f(self, x):
         self.broj_poziva_funkcije += 1
         return 0.25 * x[0][0]**4 - x[0][0]**2 + 2 * x[0][0] + (x[0][1] - 1)**2
      
      def grad_f(self, x):
         self.broj_poziva_gradijenta += 1
         return Matrica(1, 2, [[x[0][0]**3 - 2 * x[0][0] + 2,2 * (x[0][1] - 1)]])

      def hess_f(self, x):
         self.broj_poziva_hesse += 1
         return Matrica(2, 2, [[3 * x[0][0]**2 - 2, 0],[0, 2]])

   #prvi zadatak
   print("\n zadatak 1. \n")

   funkcija1 = TrecaFunkcija()
   x0 = Matrica(1, 2, [[0, 0]])

   rjesenje = gradijentni_spust(funkcija1, x0, metoda_zlatnog_reza=False)
   print("Rješenje grad spustom bez zlatnog reza:", rjesenje)
   print("Broj poziva funkcije:", funkcija1.broj_poziva_funkcije)
   print("Broj poziva gradijenta:", funkcija1.broj_poziva_gradijenta)

   funkcija1.reset()

   rjesenje = gradijentni_spust(funkcija1, x0, metoda_zlatnog_reza=True)
   print("\n" + "Rješenje grad spustom sa zlatnim rezom:", rjesenje)
   print("Broj poziva funkcije:", funkcija1.broj_poziva_funkcije)
   print("Broj poziva gradijenta:", funkcija1.broj_poziva_gradijenta)

   funkcija1.reset()

   #2. zadatak
   print("\n zadatak 2. \n")

   funkcija21 = PrvaFunkcija()
   funkcija22 = DrugaFunkcija()
   x01 = Matrica(1, 2, [[-1.9, 2]])
   x02 = Matrica(1, 2, [[0.1, 0.3]])

   rjesenje1 = gradijentni_spust(funkcija21, x01, metoda_zlatnog_reza=True)
   rjesenje2 = gradijentni_spust(funkcija22, x02, metoda_zlatnog_reza=True)
   print("Rješenje prve funkcije grad spustom:", rjesenje1)
   print("Broj poziva funkcije:", funkcija21.broj_poziva_funkcije)
   print("Broj poziva gradijenta:", funkcija21.broj_poziva_gradijenta)
   print("\nRješenje druge funkcije grad spustom: ", rjesenje2)
   print("Broj poziva funkcije:", funkcija22.broj_poziva_funkcije)
   print("Broj poziva gradijenta:", funkcija22.broj_poziva_gradijenta)
   funkcija21.reset()
   funkcija22.reset()

   rjesenje1 = newton_raphson(funkcija21, funkcija21.grad_f, funkcija21.hess_f, x01, metoda_zlatnog_reza=True)
   rjesenje2 = newton_raphson(funkcija22, funkcija22.grad_f, funkcija22.hess_f, x02, metoda_zlatnog_reza=True)
   print("\nRješenje prve funkcije newtonovom metodom:", rjesenje1)
   print("Broj poziva funkcije:", funkcija21.broj_poziva_funkcije)
   print("broj poziva gradijenta prve:", funkcija21.broj_poziva_gradijenta)
   print("broj poziva hessa prve: ", funkcija21.broj_poziva_hesse)
   print("\nRješenje druge newton:", rjesenje2)
   print("Broj poziva funkcije:", funkcija22.broj_poziva_funkcije)
   print("broj poziva gradijenta druge:", funkcija22.broj_poziva_gradijenta)
   print("broj poziva hessa druge: ", funkcija22.broj_poziva_hesse)

   funkcija21.reset()
   funkcija22.reset()

   #3. zadatak
   print("\n zadatak 3. \n")

   funkcija31 = CetvrtaFunkcija()
   x01 = Matrica(1, 2, [[3, 3]])
   x02 = Matrica(1, 2, [[1, 2]])

   rjesenje31 = newton_raphson(funkcija31, funkcija31.grad_f, funkcija31.hess_f, x01, metoda_zlatnog_reza=False)
   print("Rješenje funkcije newtonovom metodom bez zlatnog reza za (3,3):", rjesenje31)
   print("Broj poziva funkcije:", funkcija31.broj_poziva_funkcije)
   print("broj poziva gradijenta:", funkcija31.broj_poziva_gradijenta)
   print("broj poziva hessa: ", funkcija31.broj_poziva_hesse)

   funkcija31.reset()

   rjesenje32  = newton_raphson(funkcija31, funkcija31.grad_f, funkcija31.hess_f, x02, metoda_zlatnog_reza=False)
   print("\nRješenje funkcije newtonovom metodom bez zlatnog reza za (1,2):", rjesenje32)
   print("Broj poziva funkcije:", funkcija31.broj_poziva_funkcije)
   print("broj poziva gradijenta:", funkcija31.broj_poziva_gradijenta)
   print("broj poziva hessa: ", funkcija31.broj_poziva_hesse)

   funkcija31.reset()

   rjesenje33 = newton_raphson(funkcija31, funkcija31.grad_f, funkcija31.hess_f, x01, metoda_zlatnog_reza=True)
   print("\nRješenje funkcije newtonovom metodom sa zlatnim rezom za (3,3):", rjesenje33)
   print("Broj poziva funkcije:", funkcija31.broj_poziva_funkcije)
   print("broj poziva gradijenta:", funkcija31.broj_poziva_gradijenta)
   print("broj poziva hessa: ", funkcija31.broj_poziva_hesse)

   funkcija31.reset()

   rjesenje34 = newton_raphson(funkcija31, funkcija31.grad_f, funkcija31.hess_f, x02, metoda_zlatnog_reza=True)
   print("\nRješenje funkcije newtonovom metodom sa zlatnim rezom za (1,2):", rjesenje34)
   print("Broj poziva funkcije:", funkcija31.broj_poziva_funkcije)
   print("broj poziva gradijenta:", funkcija31.broj_poziva_gradijenta)
   print("broj poziva hessa: ", funkcija31.broj_poziva_hesse)

   funkcija31.reset()

   # zadatak 4.
   print("\n zadatak 4. \n")


   class Funkcije4():
      def __init__(self):
         self.broj_poziva = 0
         self.grad_num = 0
      def G(self, x):
         self.broj_poziva += 1
         return Matrica(2, 1, [[10 * ((x[0][1] - x[0][0]**2))],[1 - x[0][0]]])

      def J(self, x):
         self.grad_num += 1
         return Matrica(2, 2, [[-20 * x[0][0], 10], [-1, 0]])

   x40 = Matrica(1, 2, [[-1.9, 2]])
   funkcija4 = Funkcije4()
   rjesenje4 = gauss_newton(funkcija4, x40, metoda_zlatnog_reza=False)
   print("Rješenje bez zlatnog reza za (-1.9,2):", rjesenje4)

   rjesenje4 = gauss_newton(funkcija4, x40, metoda_zlatnog_reza=True)
   print("Rješenje sa zlatnim rezom za (-1.9,2):", rjesenje4)

   # zadatak 5.
   print("\n zadatak 5. \n")
   class Funkcije5():
      def __init__(self):
         self.broj_poziva = 0
         self.grad_num = 0
      def G(self, x):
         self.broj_poziva += 1
         return Matrica(2, 1, [[x[0][0]**2 + x[0][1]**2 - 1],[ x[0][1] - x[0][0]**2]])

      def J(self, x):
         self.grad_num += 1
         return Matrica(2, 2, [[2 * x[0][0], 2 * x[0][1]],
                           [-2 * x[0][0], 1]])

   x01 = Matrica(1, 2, [[-2.0, 2.0]])
   x02 = Matrica(1, 2, [[2.0, 2.0]])
   x03 = Matrica(1, 2, [[2.0, -2.0]])
   funkcija5 = Funkcije5()

   rjesenje51 = gauss_newton(funkcija5, x01, metoda_zlatnog_reza=False)
   print("Rješenje bez zlatnog reza za (-2,2):", rjesenje51)

   rjesenje52 = gauss_newton(funkcija5, x01, metoda_zlatnog_reza=True)
   print("\nRješenje sa zlatnim rezom za (-2,2):", rjesenje52)

   rjesenje53 = gauss_newton(funkcija5, x02, metoda_zlatnog_reza=False)
   print("\nRješenje bez zlatnog reza za (2,2):", rjesenje53)

   rjesenje54 = gauss_newton(funkcija5, x02, metoda_zlatnog_reza=True)
   print("\nRješenje sa zlatnim rezom za (2,2):", rjesenje54)
   
   rjesenje55 = gauss_newton(funkcija5, x03, metoda_zlatnog_reza=False)
   print("\nRješenje bez zlatnog reza za (2,-2):", rjesenje55)

   rjesenje56 = gauss_newton(funkcija5, x03, metoda_zlatnog_reza=True)
   print("\nRješenje sa zlatnim rezom za (2,-2):", rjesenje56)

   #zadatak 6.
   print("\n zadatak 6. \n")

   t_values = [1, 2, 3, 5, 6, 7]
   y_values = [3, 4, 4, 5, 6, 8]

   class Funkcije6():
      def __init__(self):
         self.grad_num = 0
         self.broj_poziva = 0
      def G(self, x):
         self.broj_poziva += 1
         G_values = [
            [x[0][0] * np.exp(x[0][1] * t) + x[0][2] - y] for t, y in zip(t_values, y_values)]
         return Matrica(len(G_values), 1, G_values)

      def J(self, x):
         self.grad_num += 1
         J_values = [[np.exp(x[0][1] * t), x[0][0] * t * np.exp(x[0][1] * t), 1] for t in t_values ]
         return Matrica(len(t_values), 3, J_values)

   x0_6 = Matrica(1, 3, [[1, 1, 1]])
   funkcija6 = Funkcije6()
   rjesenje6 = gauss_newton(funkcija6, x0_6, metoda_zlatnog_reza=False)
   print("Rješenje bez metode zlatnog reza parametri:", rjesenje6)

   rjesenje62 = gauss_newton(funkcija6, x0_6, metoda_zlatnog_reza=True)
   print("Rješenje sa metodom zlatnog reza parametri:", rjesenje62)

   plt.scatter(t_values, y_values, color='red', label='Podaci')

   t_model = np.linspace(min(t_values), max(t_values), 100)
   y_model = [
      rjesenje6[0][0] * np.exp(rjesenje6[0][1] * t) + rjesenje6[0][2]
      for t in t_model
   ]
   plt.plot(t_model, y_model)

   plt.xlabel('t')
   plt.ylabel('y')
   plt.legend()
   plt.title('Zadatak 6: gauss-newton')
   plt.show()



if __name__ == "__main__":
   main()