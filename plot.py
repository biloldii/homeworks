import sys
import numpy as np
import sympy as sp
from PySide6.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, QLabel
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D  
from scipy import integrate


class PlotWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wolfram Father - 3D Plot")

        self.input = QLineEdit()
        self.input.setPlaceholderText("Enter function (in x and/or z), e.g. x**2 + z**2")

        self.point_a = QLineEdit()
        self.point_a.setPlaceholderText("Lower limit a for x (e.g. 0)")

        self.point_b = QLineEdit()
        self.point_b.setPlaceholderText("Upper limit b for x (e.g. 2)")

        self.area_label = QLabel("Area under the curve (1D x only): ")

        self.button = QPushButton("PLOT")


        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        toolbar = NavigationToolbar(self.canvas, self)

      
        layout = QVBoxLayout()
        layout.addWidget(self.input)

        limits_layout = QHBoxLayout()
        limits_layout.addWidget(self.point_a)
        limits_layout.addWidget(self.point_b)
        layout.addLayout(limits_layout)

        layout.addWidget(self.button)
        layout.addWidget(self.canvas)
        layout.addWidget(self.area_label)
        layout.addWidget(toolbar)
        self.setLayout(layout)

        self.button.clicked.connect(self.plot)

    def plot(self):
        expression = self.input.text()
        a = float(self.point_a.text())
        b = float(self.point_b.text())

    
        x_vals = np.linspace(-10, 10, 100)
        z_vals = np.linspace(-10, 10, 100)
        x, z = np.meshgrid(x_vals, z_vals)

        try:
       
            y = eval(expression, {"x": x, "z": z, "np": np, "__builtins__": {}})
        except Exception as e:
            print("Invalid function:", e)
            return

        try:
            x_sym = sp.Symbol("x")
            f_sym = eval(expression, {"x": x_sym, "sp": sp, "np": np, "__builtins__": {}})
            f_lamb = sp.lambdify(x_sym, f_sym, modules=["numpy"])
            area, _ = integrate.quad(f_lamb, a, b)
            self.area_label.setText(f"Area from {a} to {b}: {area:.4f}")
        except:
            self.area_label.setText("Area only for functions in x")

      
        self.figure.clear()
        ax = self.figure.add_subplot(111, projection='3d')
        ax.plot_surface(x, z, y, cmap='viridis', edgecolor='none', alpha=0.8)

        ax.set_xlabel("x")
        ax.set_ylabel("z")
        ax.set_zlabel("y = f(x, z)")
        ax.set_title(f"3D Plot of: {expression}")

        self.canvas.draw()



app = QApplication(sys.argv)
window = PlotWindow()
window.show()
sys.exit(app.exec())
