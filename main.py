def run_simulation(a1, a0, b2, b1, b0, Kp, Ki, f, phi, tmax, dt,):
    import numpy as np
    import control as ct
    from scipy.signal import square
    from scipy.signal import sawtooth
    


    #TODO: samodzielne wyprowadznie moaciezy A, B, C, D(na kartce) 

    # Licznik i mianownik transmitancji Gp(s)
    Gp_licznik = [a1, a0]
    Gp_mianownik = [b2, b1, b0]

    # Tworzenie obiektu transmitancji
    Gp = ct.tf(Gp_licznik, Gp_mianownik)

    

    # Licznik i mianownik PI
    Gc_licznik = [Kp, Ki]
    Gc_mianownik = [1, 0]  # odpowiada 1/s

    # Transmitancja PI
    Gc = ct.tf(Gc_licznik, Gc_mianownik)

    # Połączenie szeregowe: C(s) * G(s)
    Go = ct.series(Gc, Gp)

    Gz = ct.feedback(Go, 1)
    if max(np.roots(Gz.den[0][0])) < 0:
        print("Układ jest stabilny")

    # Przekształcenie na model stanu
    ss_model = ct.tf2ss(Gz)
    A, B, C, D = ss_model.A, ss_model.B, ss_model.C, ss_model.D
   
    T = np.arange(0, tmax, dt) # wektor czasu
    
    # Liczba elementów w wektorze T
    num_elements = len(T)

    phi = np.radians(phi)  # faza w radianach (aktualnie 90 stopni)
    duty_cycle = 0.5  # współczynnik wypełnienia dla sygnału prostokątnego
    Usin = np.sin(2 * np.pi * f * T + phi)
    Uprostokotny = square(2 * np.pi * f * T + phi, duty=duty_cycle)  # squre generije sygnal o wartosciach 1 i -1 spytac czy ma być 0 i 1 
    Utrojkatny = sawtooth(2 * np.pi * f * T + phi, width=0.5)  # sygnał trójkątny z częstotliwością f i przesunięciem fazowym phi
    
    A = dt * A
    B = dt * B
    # Zerowe warunki początkowe
    X = np.zeros((A.shape[0], 1))  # Wektor stanu
    Xp = np.zeros((A.shape[0], 1))  # Wektor pomocniczy
    #testy
    U = np.ones((num_elements, 1))
    input_signal = U   
    output_signal = []
    for i in range(num_elements-1):
        #krok próbny
        Xp = Xp + A @ Xp + B * U[i]
        #krok wlaściwy
        X = Xp + 0.5 * (A @ X + B * U[i]  + A @ Xp + B * U[i+1])
        Ystate = C @ X + D * U[i]
        output_signal.append(Ystate.item())  # Dodaj wynik do tablicy
 
 # Dodanie ostatniego punktu do output_signal
    Ystate = C @ X + D * input_signal[-1]
    output_signal.append(Ystate.item())

    return T, input_signal, output_signal