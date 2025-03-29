from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QGridLayout, QApplication, QWidget, QScrollArea
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QSize

from Storage.StorageManager import StorageMan
from Storage.AniList import AniList
from Entities.Anime import Anime
from GUI.AniCard import AniCard

class ListTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Create scroll area
        scrollArea = QScrollArea(self)
        scrollArea.setWidgetResizable(True)

        # Container for anime cards
        self.container = QWidget()
        self.container_layout = QGridLayout()
        self.container_layout.setSpacing(15)

        # Load anime list
        self.StoreMan = StorageMan()
        self.anilis = AniList()
        self.StoreMan.LoadList(aniList=self.anilis)

        # Create AniCards and add them to the grid
        self.loadedCards = [AniCard(card) for card in self.anilis.WatchList]

        columns = 2
        for index, card in enumerate(self.loadedCards):
            row = index // columns
            col = index % columns
            card.remove_signal.connect(self.__RemoveAnime)
            self.container_layout.addWidget(card, row, col)

        self.container.setLayout(self.container_layout)
        scrollArea.setWidget(self.container)

        layout.addWidget(scrollArea)
        self.setLayout(layout)

    def __RemoveAnime(self, card):
        self.container_layout.removeWidget(card)
        card.deleteLater()
        self.loadedCards.remove(card)
        self.anilis.RemoveAnime(card.anime)
        self.StoreMan.SaveList(self.anilis)

        columns = 2
        for index, card in enumerate(self.loadedCards):
            row = index // columns
            col = index % columns
            self.container_layout.addWidget(card, row, col)

        self.container.updateGeometry()

