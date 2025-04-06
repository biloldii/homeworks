import sys
from PySide6.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QWidget
from PySide6.QtGui import QPalette, QColor

class StickyNotes(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sticky Notes")
         
     
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("blue"))  
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Write your notes here...")

     
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        self.setLayout(layout)


app = QApplication(sys.argv)
window = StickyNotes()
window.show()
sys.exit(app.exec())
