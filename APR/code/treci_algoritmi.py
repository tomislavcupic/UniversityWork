import numpy as np
from abc import ABC, abstractmethod
from matrica import Matrica
from drugi import zlatni_rez
from math import sqrt

class CiljnaFunkcija(ABC):
    def __init__(self):
        self.broj_poziva_funkcije = 0
        self.broj_poziva_gradijenta = 0
        self.broj_poziva_hesse = 0

    def reset(self):
        self.broj_poziva_funkcije = 0
        self.broj_poziva_gradijenta = 0
        self.broj_poziva_hesse = 0

    @abstractmethod
    def f(self, x):
        pass

    @abstractmethod
    def grad_f(self, x):
        pass

    @abstractmethod
    def hess_f(self, x):
        pass

    def broj_poziva(self):
        return {
            "funkcija": self.broj_poziva_funkcije,
            "gradijent": self.broj_poziva_gradijenta,
            "hesse": self.broj_poziva_hesse,
        }

def gradijentni_spust(funkcija, x0, epsilon=1e-6, metoda_zlatnog_reza=False, max_iter=30000):
    x = x0
    best_value = funkcija.f(x)
    div_count = 0
    for count in range(1,max_iter):
        grad = funkcija.grad_f(x)
        grad_norm = sqrt(sum(data**2 for data in grad.data[0]))

        if grad_norm < epsilon:
           return x
        
        if metoda_zlatnog_reza:
            def g(lam):
                return funkcija.f(x + lam*grad)
            lambda_opt = zlatni_rez(g, a=0)
        else:
            lambda_opt = 1.0
        x = x + lambda_opt * grad
        new_value = funkcija.f(x)
        if (new_value - best_value) >= 0:
            div_count += 1 
            if div_count > 9:
                print("divergira.")
                return x
        else:
            div_count = 0
        best_value = new_value

    print("Konvergira ali presporo")
    return x

def newton_raphson(funkcija, grad_f, hess_f, x0, epsilon=1e-6, metoda_zlatnog_reza=False, max_iter=10000):
    x = x0
    best_value = funkcija.f(x)
    div_count = 0
    for count in range(max_iter):
        grad = grad_f(x)
        grad = grad * -1
        hess = hess_f(x)
        
        delta_x = hess.solve(grad.T())
        norm_delta_x = sqrt(sum(data**2 for data in delta_x.data[0]))
        if norm_delta_x < epsilon:
            return x
        
        if metoda_zlatnog_reza:
            def g(lam):
                return funkcija.f(x + lam * delta_x.T())
            
            lambda_opt = zlatni_rez(g, a=0)
        else:
            lambda_opt = 1.0
        
        x = x + lambda_opt * delta_x.T()
        new_value = funkcija.f(x)
        if (new_value - best_value) >= 0:
            div_count += 1 
            if div_count > 9:
                print("divergira.")
                return x
        else:
            div_count = 0
            best_value = new_value

    print("Maksimalni broj iteracija dosegnut.")
    return x

def gauss_newton(f, x0, epsilon=1e-6, metoda_zlatnog_reza=False, max_iter=10000):
    x = x0
    best_value = sqrt(sum(data**2 for data in f.G(x).data[0]))
    div_count = 0
    
    for count in range(max_iter):
        J_x = f.J(x)
        G_x = f.G(x)
        A = J_x.T() * J_x
        g = J_x.T() * G_x
        g = -1 * g
        delta_x = A.solve(g)
        if g is None:
            print("divergencija ili singularna matrica")
            return None
        norm_delta_x = sqrt(sum(data**2 for data in g.data[0])) 
        if norm_delta_x < epsilon:
            print("broj poziva funkcije:" , f.broj_poziva)
            print("broj poziva gradijenta:", f.grad_num)
            return x
        
        if metoda_zlatnog_reza:
            def g1(lam):
                g_t = f.G(x + lam * delta_x.T())
                value = sum(data[0]**2 for data in g_t.data)
                return value
            lambda_opt = zlatni_rez(g1, a=0)
        else:
            lambda_opt = 1.0 
        x = x + (lambda_opt * delta_x.T())
        new_value = sqrt(sum(data**2 for data in f.G(x).data[0]))
        if (new_value - best_value) >= 0:
            div_count += 1
            if div_count > 9:
                print("Postupak divergirano - nema poboljšanja u 10 uzastopnih iteracija.")
                print("broj poziva funkcije:" , f.broj_poziva)
                print("broj poziva gradijenta:", f.grad_num)
                return x
        else:
            div_count = 0
            best_value = new_value
    
    print("Maksimalni broj iteracija dosegnut.")
    return x