import numpy as np
import control as ct

# Przykładowe współczynniki transmitancji
a1, a0 = 2.0, 1.0   # licznik
b2, b1, b0 = 1.0, 3.0, 2.0  # mianownik

# Licznik i mianownik transmitancji Gp(s)
Gp_licznik = [a1, a0]
Gp_mianownik = [b2, b1, b0]

# Tworzenie obiektu transmitancji
Gp = ct.tf(Gp_licznik, Gp_mianownik)

Kp, Ki = 1.5, 0.5  # Przykładowe wartości regulatora PI

# Licznik i mianownik PI
Gc_licznik = [Kp, Ki]
Gc_mianownik = [1, 0]  # odpowiada 1/s

# Transmitancja PI
Gc = ct.tf(Gc_licznik, Gc_mianownik)

# Połączenie szeregowe: C(s) * G(s)
Go = ct.series(Gc, Gp)

Gz = ct.feedback(Go, 1)


# Przekształcenie na model stanu
ss_model = ct.tf2ss(Gz)
A, B, C, D = ss_model.A, ss_model.B, ss_model.C, ss_model.D
print("Macierz A:\n", A)
print("Macierz B:\n", B)
print("Macierz C:\n", C)
print("Macierz D:\n", D)
