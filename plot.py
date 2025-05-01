import sys
import numpy as np
import sympy as sp
from PySide6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from matplotlib.figure import Figure
from scipy import integrate


class PlotWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wolfram Father")

        self.input = QLineEdit()
        self.input.setPlaceholderText("enter function...")
        self.point_a = QLineEdit()
        self.point_a.setPlaceholderText("enter limit a...")
        self.point_b = QLineEdit()
        self.point_b.setPlaceholderText("enter limit b...")
        self.area_label = QLabel("integral equals to...")
        self.button = QPushButton("Draw")

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout()
        layout.addWidget(self.input)

        point_inputs = QHBoxLayout()
        point_inputs.addWidget(self.point_a)
        point_inputs.addWidget(self.point_b)
        layout.addLayout(point_inputs)

        layout.addWidget(self.button)
        layout.addWidget(self.canvas)
        layout.addWidget(self.area_label)
       

        self.setLayout(layout)
        self.init_style()

        self.button.clicked.connect(self.plot)

    def plot(self):
        expression = self.input.text()
        point_a = float(self.point_a.text())
        point_b = float(self.point_b.text())
        x = np.linspace(-10, 10, 400)

        try:
            y = eval(expression, {"x": x, "np": np, "__builtins__": {}})
            dfdx = np.gradient(y, x)
            
            function = lambda x: eval(expression)
            area = integrate.quad(function, point_a, point_b)
        except Exception as e:
            print("Invalid function:", e)
            return

        self.figure.clear()
        axes = self.figure.add_subplot(111)
        axes.plot(x, y, color="blue")
        axes.plot(x, dfdx, color="red")
        
        axes.fill_between(
            x, 
            y, 
            0,
            where=(x > point_a) & (x < point_b),
            color="blue", alpha=0.5
        )
        
        self.area_label.setText(str(area))
        axes.grid(True)
        axes.legend()
        axes.set_title(f"y = {expression}")
        self.canvas.draw()

    def init_style(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                border: 1px solid #dcdcdc;
            } 
            QPushButton {
                background-color: #0078d7;
                color: white;
                font-size: 18px; 
                font-family: "Arial", sans-serif; 
                padding: 10px 20px;
                border-radius: 5px;
                border: none;
            }
            QPushButton::pressed {
                background-color: #005a9e;
                color: white;
                border: 2px solid #ffcc00;
            }
            QLineEdit {
                font-size: 18px;
                font-family: "Courier New", monospace;
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 4px;
                background-color: #ffffff;
            }
            QLabel {
                font-size: 18px;
                font-family: "Arial", sans-serif;
                color: #333333;
                padding: 5px;
                text-align: center;
            }
        """)


        
app = QApplication(sys.argv)
window = PlotWindow()
window.show()
sys.exit(app.exec())