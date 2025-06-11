def run_simulation(a1, a0, b2, b1, b0, Kp, Ki, signal_type, f, phi, tmax, dt,):
    import numpy as np
    import control as ct
    from scipy.signal import square, sawtooth

    #TODO: samodzielne wyprowadznie macierzy A, B, C, D(na kartce) 

    Gp_licznik = [a1, a0]
    Gp_mianownik = [b2, b1, b0]    
    
    Gc_licznik = [Kp, Ki]
    Gc_mianownik = [1, 0]  

    Go_licznik = np.polymul(Gc_licznik, Gp_licznik)
    Go_mianownik = np.polymul(Gc_mianownik, Gp_mianownik)

    feedback_licznik = Go_licznik
    feedback_mianownik = np.polyadd(Go_mianownik, Go_licznik)


    if max(np.roots(feedback_mianownik)) < 0:
        print("Układ jest stabilny")

    A = np.array([[0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [-feedback_mianownik[3] / feedback_mianownik[0], -feedback_mianownik[2] / feedback_mianownik[0], -feedback_mianownik[1] / feedback_mianownik[0]]])
    B = np.array([[0.0], 
         [0.0], 
         [1.0]])
    C = np.array([[feedback_licznik[2] / feedback_mianownik[0], feedback_licznik[1] / feedback_mianownik[0], feedback_licznik[0] / feedback_mianownik[0]]])
    D = np.array([0.0])
   
    T = np.arange(0, tmax, dt) 
    
    
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
        raise ValueError("Unknown signal type")
    
    input_signal = U   
    output_signal = []
    for i in range(num_elements-1):
        Xp = Xp + A @ Xp + B * U[i]
        X = Xp + ((A @ X + B * U[i]  + A @ Xp + B * U[i+1])/2)
        Ystate = C @ X + D * U[i]
        output_signal.append(Ystate.item())  
 
    Ystate = C @ X + D * U[-1]
    output_signal.append(Ystate.item())

    return T, input_signal, output_signal