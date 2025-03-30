from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QGridLayout, QApplication, QWidget, QLineEdit, QScrollArea
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

        toolBoxLayout = QHBoxLayout()
        toolBoxLayout.setAlignment(Qt.AlignCenter)

        self.SearchBar = QLineEdit()
        self.SearchBar.setPlaceholderText("Search...")
        self.SearchBar.setFixedSize(QSize(1000,40))
        self.SearchBar.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding: 5px;
                border-radius: 4px;
                background-color: #DEE0E0;
                color: dark-gray;
            }
        """)

        self.SearchButton = QPushButton("Search")
        self.SearchButton.clicked.connect(self.SearchAnime)
        self.SearchButton.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                padding: 10px;
                border-radius: 4px;
                background-color: #DEE0E0;
            } QPushButton::Hover {
                background-color: #b4b8b8;
            }
        """)

        self.FilterButton = QPushButton("Filter")
        self.FilterButton.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                padding: 10px;
                border-radius: 4px;
                background-color: #DEE0E0;
            } QPushButton::Hover {
                background-color: #b4b8b8;
            }
        """)

        self.ResetButton = QPushButton("Reset")
        self.ResetButton.clicked.connect(self.ResetCards)
        self.ResetButton.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                padding: 10px;
                border-radius: 4px;
                background-color: #DEE0E0;
            } QPushButton::Hover {
                background-color: #b4b8b8;
            }
        """)


        toolBoxLayout.addWidget(self.SearchBar)
        toolBoxLayout.addWidget(self.SearchButton)
        toolBoxLayout.addWidget(self.FilterButton)
        toolBoxLayout.addWidget(self.ResetButton)

        # Create scroll area
        scrollArea = QScrollArea(self)
        scrollArea.setWidgetResizable(True)

        # Container for anime cards
        self.container = QWidget()
        self.container_layout = QGridLayout()
        self.container_layout.setSpacing(15)

        self.NotFoundLabel = QLabel("No Anime Found...")
        self.NotFoundLabel.setAlignment(Qt.AlignCenter)
        self.NotFoundLabel.setStyleSheet("""
            QLabel {
                font-size: 30px;
                color: gray;
            }
        """)

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

        layout.addLayout(toolBoxLayout)
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

    def ResetCards(self):
        self.SearchBar.setText("")
        while self.container_layout.count():
            item = self.container_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        columns = 2
        for index, card in enumerate(self.loadedCards):
            row = index // columns
            col = index % columns
            self.container_layout.addWidget(card, row, col)

        if self.NotFoundLabel in [self.container_layout.itemAt(i).widget() for i in range(self.container_layout.count())]:
            self.container_layout.removeWidget(self.NotFoundLabel)
            self.NotFoundLabel.setParent(None)

        self.container.updateGeometry()


    def SearchAnime(self):
        search_text = self.SearchBar.text().strip().lower()

        while self.container_layout.count():
            item = self.container_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
        results = [card for card in self.loadedCards if search_text in card.anime.Title.lower()]
        if len(results) > 0:
            columns = 2
            for index, card in enumerate(results):
                row = index // columns
                col = index % columns
                self.container_layout.addWidget(card, row, col)
        else:
            self.container_layout.addWidget(self.NotFoundLabel)

        self.container.updateGeometry()

