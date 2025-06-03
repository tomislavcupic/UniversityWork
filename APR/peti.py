from matrica import Matrica
import numpy as np
import matplotlib.pyplot as plt
from peti_algoritmi import *

def main():
   print("prvi zadatak: \n")

   matrica1a = Matrica.read_from_file("matrica_1.txt")
   matrica1b = Matrica.read_from_file("matrica_2.txt")
   pocetno_stanje1 = Matrica(2, 1, [[1], [1]])
   r1 = lambda t: Matrica(data=[[1], [1]])

   print("Euler \n")
   xv11, t11 = euler(matrica1a, matrica1b, r1, pocetno_stanje1, 10, 0.01)
   ljepsi_print(xv11, t11, 100)
   error1 = cumulative_error(xv11, t11, pocetno_stanje1)
   print(float(error1[0]), float(error1[1]))

   print("\n Obrnuti euler \n")
   xv12, t12 = obrnuti_euler(matrica1a, matrica1b, r1, pocetno_stanje1, 10, 0.01)
   ljepsi_print(xv12, t12)
   error2 = cumulative_error(xv12, t12, pocetno_stanje1)
   print(float(error2[0]), float(error2[1]))

   print("\n Trapezoid \n")
   xv13, t13 = trapezoid(matrica1a, matrica1b, r1, pocetno_stanje1, 10, 0.01)
   ljepsi_print(xv13, t13)
   error3 = cumulative_error(xv13, t13, pocetno_stanje1)
   print(float(error3[0]), float(error3[1]))

   print("\n Runge_Kutta4 \n")
   xv14, t14 = runge_kutta4(matrica1a, matrica1b, r1, pocetno_stanje1, 10, 0.01)
   ljepsi_print(xv14, t14)
   error4 = cumulative_error(xv14, t14, pocetno_stanje1)
   print(float(error4[0]), float(error4[1]))

   print("\n pece_euler_obrnutieuler \n")
   xv15, t15 = pece_metoda_euler_obrnuti_euler(matrica1a, matrica1b, r1, pocetno_stanje1, 10, 0.01, euler, obrnuti_euler, 2)
   pece_ljepsi_print(xv15, t15)
   error5 = cumulative_error_pece(xv15, t15, pocetno_stanje1)
   print(float(error5[0]), float(error5[1]))

   print("\n pece_euler_trapezoid \n")
   xv16, t16 = pece_metoda_euler_trapez(matrica1a, matrica1b, r1, pocetno_stanje1, 10, 0.01, euler, trapezoid, 1)
   pece_ljepsi_print(xv16, t16)
   error6 = cumulative_error_pece(xv16, t16, pocetno_stanje1)
   print(float(error6[0]), float(error6[1]))


   #----------------------------------------------------------------------------------------------------------------------------------#
   print("\n Drugi zadatak: \n")

   matrica2a = Matrica(data=[[0, 1],[-200, -102]])
   matrica2b = Matrica(data=[[0, 0], [0, 0]])
   pocetno_stanje2 = Matrica(2, 1, [[1], [-2]])
   r1 = lambda t: Matrica(data=[[1], [1]])

   print("Euler \n")
   xv21, t21 = euler(matrica2a, matrica2b, r1, pocetno_stanje2, 1, 0.1)
   ljepsi_print(xv21, t21, 1) 

   print("\n Obrnuti euler \n")
   xv22, t22 = obrnuti_euler(matrica2a, matrica2b, r1, pocetno_stanje2, 1, 0.01)
   ljepsi_print(xv22, t22, 10)

   print("\n Trapezoid \n")
   xv23, t23 = trapezoid(matrica2a, matrica2b, r1, pocetno_stanje2, 1, 0.1)
   ljepsi_print(xv23, t23, 1)

   print("\n Runge_Kutta4 \n")
   xv24, t24 = runge_kutta4(matrica2a, matrica2b, r1, pocetno_stanje2, 1, 0.1)
   ljepsi_print(xv24, t24, 1)

   print("\n pece_euler_obrnutieuler \n")
   xv25, t25 = pece_metoda_euler_obrnuti_euler(matrica2a, matrica2b, r1, pocetno_stanje2, 1, 0.1, euler, obrnuti_euler, 2)
   pece_ljepsi_print(xv25, t25, 1)
   
   print("\n pece_euler_trapezoid \n")
   xv26, t26 = pece_metoda_euler_trapez(matrica2a, matrica2b, r1, pocetno_stanje2, 1, 0.1, euler, trapezoid, 1)
   pece_ljepsi_print(xv26, t26, 1)

   #------------------------------------------------------------------------------------------------------------------#
   print("\n Treci zadatak: \n")

   matrica3a = Matrica(data=[[0, -2],[1, -3]])
   matrica3b = Matrica(data=[[2, 0], [0, 3]])
   pocetno_stanje3 = Matrica(2, 1, [[1], [3]])
   r1 = lambda t: Matrica(data=[[1], [1]])

   print("Euler \n")
   xv31, t31 = euler(matrica3a, matrica3b, r1, pocetno_stanje3, 10, 0.01)
   ljepsi_print( xv31, t31) 

   print("\n Obrnuti euler \n")
   xv32, t32 = obrnuti_euler(matrica3a, matrica3b, r1, pocetno_stanje3,10, 0.01)
   ljepsi_print(xv32, t32)

   print("\n Trapezoid \n")
   xv33, t33 = trapezoid(matrica3a, matrica3b, r1, pocetno_stanje3, 10, 0.01)
   ljepsi_print(xv33, t33, 100)

   print("\n Runge_Kutta4 \n")
   xv34, t34 = runge_kutta4(matrica3a, matrica3b, r1, pocetno_stanje3, 10, 0.01)
   ljepsi_print(xv34, t34, 100)
   
   print("\n pece_euler_obrnutieuler \n")
   xv35, t35 = pece_metoda_euler_obrnuti_euler(matrica3a, matrica3b, r1, pocetno_stanje3, 10, 0.01, euler, obrnuti_euler, 2)
   pece_ljepsi_print(xv35, t35, 100)
   
   print("\n pece_euler_trapezoid \n")
   xv36, t36 = pece_metoda_euler_trapez(matrica3a, matrica3b, r1, pocetno_stanje3, 10, 0.01, euler, trapezoid, 1)
   pece_ljepsi_print(xv36, t36, 100)

   #-------------------------------------------------------------------------------------------------------------#
   print("\n Cetvrti zadatak: \n")

   matrica4a = Matrica(data=[[1, -5],[1, -7]])
   matrica4b = Matrica(data=[[5, 0], [0, 3]])
   pocetno_stanje4 = Matrica(data=[[-1], [3]])
   r4 = lambda t: Matrica(data=[[t], [t]])

   print("Euler \n")
   xv41, t41 = euler(matrica4a, matrica4b, r4, pocetno_stanje4, 1, 0.01)
   ljepsi_print( xv41, t41, 10) 

   print("\n Obrnuti euler \n")
   xv42, t42 = obrnuti_euler(matrica4a, matrica4b, r4, pocetno_stanje4, 1, 0.01)
   ljepsi_print(xv42, t42, 10)

   print("\n Trapezoid \n")
   xv43, t43 = trapezoid(matrica4a, matrica4b, r4, pocetno_stanje4, 1, 0.01)
   ljepsi_print(xv43, t43, 10)

   print("\n Runge_Kutta4 \n")
   xv44, t44 = runge_kutta4(matrica4a, matrica4b, r4, pocetno_stanje4, 1, 0.01)
   ljepsi_print(xv44, t44, 10)

   print("\n pece_euler_obrnutieuler \n")
   xv45, t45 = pece_metoda_euler_obrnuti_euler(matrica4a, matrica4b, r4, pocetno_stanje4, 1, 0.01, euler, obrnuti_euler, 2)
   pece_ljepsi_print(xv45, t45, 10)
   
   print("\n pece_euler_trapezoid \n")
   xv46, t46 = pece_metoda_euler_trapez(matrica4a, matrica4b, r4, pocetno_stanje4, 1, 0.01, euler, trapezoid, 1)
   pece_ljepsi_print(xv46, t46, 10)


   #euler prvi zadatak
   x1 = [x[0] for x in xv11]
   x2 = [x[1] for x in xv11]

   plt.figure(figsize=(10, 6))
   plt.plot(t11, x1, label='x1(t)', color='red')
   plt.plot(t11, x2, label='x2(t)', color='blue')

   plt.title('Ponašanje sustava (Eulerov postupak)')
   plt.xlabel('Vrijeme t')
   plt.ylabel('Stanja x(t)')
   plt.legend()
   plt.grid()
   plt.show()


   #euler drugi zadatak
   x1 = [x[0] for x in xv21]
   x2 = [x[1] for x in xv21]

   plt.figure(figsize=(10, 6))
   plt.plot(t21, x1, label='x1(t)', color='red')
   plt.plot(t21, x2, label='x2(t)', color='blue')

   plt.title('Ponašanje sustava (Eulerov postupak)')
   plt.xlabel('Vrijeme t')
   plt.ylabel('Stanja x(t)')
   plt.legend()
   plt.grid()
   plt.show()

   #euler treci zadatak
   x1 = [x[0] for x in xv31]
   x2 = [x[1] for x in xv31]

   plt.figure(figsize=(10, 6))
   plt.plot(t31, x1, label='x1(t)', color='red')
   plt.plot(t31, x2, label='x2(t)', color='blue')

   plt.title('Ponašanje sustava (Eulerov postupak)')
   plt.xlabel('Vrijeme t')
   plt.ylabel('Stanja x(t)')
   plt.legend()
   plt.grid()
   plt.show()

   #euler cetvrti zadatak
   x1 = [x[0] for x in xv41]
   x2 = [x[1] for x in xv41]

   plt.figure(figsize=(10, 6))
   plt.plot(t41, x1, label='x1(t)', color='red')
   plt.plot(t41, x2, label='x2(t)', color='blue')

   plt.title('Ponašanje sustava (Eulerov postupak)')
   plt.xlabel('Vrijeme t')
   plt.ylabel('Stanja x(t)')
   plt.legend()
   plt.grid()
   plt.show()

if __name__ == "__main__":
   main()
