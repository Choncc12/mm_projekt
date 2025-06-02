def run_simulation(a1, a0, b2, b1, b0, Kp, Ki, signal_type, f, phi, tmax, dt,):
    import numpy as np
    import control as ct
    from scipy.signal import square
    from scipy.signal import sawtooth
    

    Gp_licznik = [a1, a0]
    Gp_mianownik = [b2, b1, b0]
    Gp = ct.tf(Gp_licznik, Gp_mianownik)
    Gc_licznik = [Kp, Ki]
    Gc_mianownik = [1, 0]  


    Gc = ct.tf(Gc_licznik, Gc_mianownik)
    Go = ct.series(Gc, Gp)
    Gz = ct.feedback(Go, 1)
    
    if max(np.roots(Gz.den[0][0])) < 0:
        print("Układ jest stabilny")

 
    ss_model = ct.tf2ss(Gz)
    A, B, C, D = ss_model.A, ss_model.B, ss_model.C, ss_model.D
   
    T = np.arange(0, tmax, dt) # wektor czasu
    

    num_elements = len(T)

    phi = np.radians(phi)  
    duty_cycle = 0.5  
    Usin = np.sin(2 * np.pi * f * T + phi)
    Uprostokotny = square(2 * np.pi * f * T + phi, duty=duty_cycle)/2+0.5  
    Utrojkatny = sawtooth(2 * np.pi * f * T + phi, width=0.5)  
    
    A = dt * A
    B = dt * B
  
    X = np.zeros((A.shape[0], 1))  
    Xp = np.zeros((A.shape[0], 1))  
   
    U = np.ones((num_elements, 1))
    if signal_type == 0:  
        U = Usin
    elif signal_type == 1:  
        U = Uprostokotny
    elif signal_type == 2:  
        U = Utrojkatny
    else:
        raise ValueError("Nieznany typ sygnału wejściowego")
    
  
    input_signal = U   
    output_signal = []
    
    for i in range(num_elements-1):
        #krok próbny
        Xp = Xp + A @ Xp + B * U[i]
        #krok właściwy
        X = Xp + 0.5 * (A @ X + B * U[i]  + A @ Xp + B * U[i+1])
        Y = C @ X + D * U[i]
        output_signal.append(Y.item())  
 
    # Dodanie ostatniego punktu do output_signal
    Y = C @ X + D * input_signal[-1]
    output_signal.append(Y.item())

    return T, input_signal, output_signal