import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QPushButton,
    QSystemTrayIcon,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

app = QApplication(sys.argv)

# Store references to the NoteWindow objects in this, keyed by id.
active_notewindows = {}


class NoteWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notes")
        self.setWindowFlags(
            self.windowFlags()
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setStyleSheet(
            "background: #FFFF99; color: #62622f; border: 0; font-size: 16pt;"
        )
        layout = QVBoxLayout()

        buttons = QHBoxLayout()
        self.close_btn = QPushButton("×")
        self.close_btn.setStyleSheet(
            "font-weight: bold; font-size: 25px; width: 25px; height: 25px;"
        )
        self.close_btn.clicked.connect(self.close)
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        buttons.addStretch()  # Add stretch on left to push button right.
        buttons.addWidget(self.close_btn)
        layout.addLayout(buttons)

        self.text = QTextEdit()
        layout.addWidget(self.text)
        self.setLayout(layout)

        # Store a reference to this note in the active_notewindows
        active_notewindows[id(self)] = self

    def mousePressEvent(self, e):
        self.previous_pos = e.globalPosition()

    def mouseMoveEvent(self, e):
        delta = e.globalPosition() - self.previous_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.previous_pos = e.globalPosition()


def create_notewindow():
    note = NoteWindow()
    note.show()


create_notewindow()

# Create the icon
icon = QIcon("sticky-note.png")

# Create the tray
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)


def handle_tray_click(reason):
    # If the tray is left-clicked, create a new note.
    if (
        QSystemTrayIcon.ActivationReason(reason)
        == QSystemTrayIcon.ActivationReason.Trigger
    ):
        create_notewindow()


tray.activated.connect(handle_tray_click)

app.exec()