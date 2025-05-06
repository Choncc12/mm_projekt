from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout
)
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Symulacja Układu - Parametry")

        # Główne okno
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QGridLayout()
        central_widget.setLayout(layout)

        # Pola do edycji współczynników transmitancji Gp
        layout.addWidget(QLabel("Transmitancja Gp - licznik:"), 0, 0)
        self.gp_licznik_input = QLineEdit("2.0, 1.0")  # Domyślne wartości
        layout.addWidget(self.gp_licznik_input, 0, 1)

        layout.addWidget(QLabel("Transmitancja Gp - mianownik:"), 1, 0)
        self.gp_mianownik_input = QLineEdit("1.0, 3.0, 2.0")  # Domyślne wartości
        layout.addWidget(self.gp_mianownik_input, 1, 1)

        # Pola do edycji nastaw regulatora PI
        layout.addWidget(QLabel("Regulator PI - Kp:"), 2, 0)
        self.kp_input = QLineEdit("1.0")  # Domyślne wartości
        layout.addWidget(self.kp_input, 2, 1)

        layout.addWidget(QLabel("Regulator PI - Ki:"), 3, 0)
        self.ki_input = QLineEdit("1.0")  # Domyślne wartości
        layout.addWidget(self.ki_input, 3, 1)

        # Pola do edycji parametrów sygnałów wejściowych
        layout.addWidget(QLabel("Częstotliwość sygnału [Hz]:"), 4, 0)
        self.freq_input = QLineEdit("100.0")  # Domyślne wartości
        layout.addWidget(self.freq_input, 4, 1)

        layout.addWidget(QLabel("Faza sygnału [rad]:"), 5, 0)
        self.phase_input = QLineEdit("1.57")  # Domyślne wartości
        layout.addWidget(self.phase_input, 5, 1)

        # Pola do edycji czasu i kroku symulacji
        layout.addWidget(QLabel("Czas symulacji [s]:"), 6, 0)
        self.tmax_input = QLineEdit("1000")  # Domyślne wartości
        layout.addWidget(self.tmax_input, 6, 1)

        layout.addWidget(QLabel("Krok symulacji [s]:"), 7, 0)
        self.dt_input = QLineEdit("0.01")  # Domyślne wartości
        layout.addWidget(self.dt_input, 7, 1)

        # Przycisk do uruchomienia symulacji
        self.run_button = QPushButton("Uruchom symulację")
        layout.addWidget(self.run_button, 8, 0, 1, 2)

        # Połączenie przycisku z funkcją
        self.run_button.clicked.connect(self.run_simulation)

    def run_simulation(self):
        # Pobieranie danych z pól tekstowych
        a1, a0 = map(float, self.gp_licznik_input.text().split(","))
        b2, b1, b0 = map(float, self.gp_mianownik_input.text().split(","))
        kp = float(self.kp_input.text())
        ki = float(self.ki_input.text())
        freq = float(self.freq_input.text())
        phase = float(self.phase_input.text())
        tmax = float(self.tmax_input.text())
        dt = float(self.dt_input.text())

        # Przekazywanie danych do main.py
        from main import run_simulation
        run_simulation(a1, a0, b2, b1, b0, kp, ki, freq, phase, tmax, dt)

# Uruchamianie aplikacji
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())