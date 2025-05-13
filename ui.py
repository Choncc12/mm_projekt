from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QHBoxLayout, QComboBox
)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Symulacja Układu - Parametry")

        # Główne okno
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Parametry wejściowe
        input_layout = QGridLayout()
        layout.addLayout(input_layout)

        input_layout.addWidget(QLabel("Transmitancja Gp - licznik:"), 0, 0)
        self.gp_licznik_input = QLineEdit("2.0, 1.0")
        input_layout.addWidget(self.gp_licznik_input, 0, 1)

        input_layout.addWidget(QLabel("Transmitancja Gp - mianownik:"), 1, 0)
        self.gp_mianownik_input = QLineEdit("1.0, 3.0, 2.0")
        input_layout.addWidget(self.gp_mianownik_input, 1, 1)

        input_layout.addWidget(QLabel("Regulator PI - Kp:"), 2, 0)
        self.kp_input = QLineEdit("1.0")
        input_layout.addWidget(self.kp_input, 2, 1)

        input_layout.addWidget(QLabel("Regulator PI - Ki:"), 3, 0)
        self.ki_input = QLineEdit("1.0")
        input_layout.addWidget(self.ki_input, 3, 1)

        input_layout.addWidget(QLabel("Typ sygnału wejściowego:"), 4, 0)
        self.signal_type_combo = QComboBox()
        self.signal_type_combo.addItems(["Sinusoidalny", "Prostokątny", "Trójkątny"])
        input_layout.addWidget(self.signal_type_combo, 4, 1)

        input_layout.addWidget(QLabel("Częstotliwość sygnału [Hz]:"), 5, 0)
        self.freq_input = QLineEdit("100.0")
        input_layout.addWidget(self.freq_input, 5, 1)

        input_layout.addWidget(QLabel("Faza sygnału [rad]:"), 6, 0)
        self.phase_input = QLineEdit("1.57")
        input_layout.addWidget(self.phase_input, 6, 1)

        input_layout.addWidget(QLabel("Czas symulacji [s]:"), 7, 0)
        self.tmax_input = QLineEdit("10")
        input_layout.addWidget(self.tmax_input, 7, 1)

        input_layout.addWidget(QLabel("Krok symulacji [s]:"), 8, 0)
        self.dt_input = QLineEdit("0.01")
        input_layout.addWidget(self.dt_input, 8, 1)

        # Przycisk do uruchomienia symulacji
        self.run_button = QPushButton("Uruchom symulację")
        layout.addWidget(self.run_button)
        self.run_button.clicked.connect(self.run_simulation)

        # Wykresy
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def run_simulation(self):
        # Pobieranie danych z pól tekstowych
        a1, a0 = map(float, self.gp_licznik_input.text().split(","))
        b2, b1, b0 = map(float, self.gp_mianownik_input.text().split(","))
        kp = float(self.kp_input.text())
        ki = float(self.ki_input.text())
        signal_type = self.signal_type_combo.currentIndex()
        freq = float(self.freq_input.text())
        phase = float(self.phase_input.text())
        tmax = float(self.tmax_input.text())
        dt = float(self.dt_input.text())

        # Przekazywanie danych do main.py
        from main import run_simulation
        time, input_signal, output_signal = run_simulation(a1, a0, b2, b1, b0, kp, ki, signal_type, freq, phase, tmax, dt)

        # Rysowanie wykresów
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(time, input_signal, label="Sygnał wejściowy")
        ax.plot(time, output_signal, label="Odpowiedź układu")
        ax.set_xlabel("Czas [s]")
        ax.set_ylabel("Amplituda")
        ax.legend()
        self.canvas.draw()

# Uruchamianie aplikacji
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())