from PyQt5.QtWidgets import QMainWindow, QFrame, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QGridLayout, QApplication, QWidget
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QSize

class SearchTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        label = QLabel("This is the Search Tab")
        layout.addWidget(label)

        self.setLayout(layout)