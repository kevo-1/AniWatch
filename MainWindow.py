import sys
from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QGridLayout, QApplication, QWidget,QTabWidget
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QSize

from GUI.ListTab import ListTab
from GUI.SearchTab import SearchTab


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('AniWatchList')
        self.setFixedSize(QSize(1500,800))
        
        self.tabs = QTabWidget()
        self.tabs.addTab(ListTab(), "Anime List")
        self.tabs.addTab(SearchTab(), "Search Anime")
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
