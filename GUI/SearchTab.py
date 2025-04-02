from PyQt5.QtWidgets import QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout, QScrollArea, QWidget
from PyQt5.QtCore import Qt, QSize

from DataFetch.ReteriveAni import searchAnime
from GUI.AniSearchCard import AniSearchCard
from Storage.StorageManager import StorageMan
from Storage.AniList import AniList
from GUI.ListTab import ListTab

class SearchTab(QWidget):
    def __init__(self, anilist: AniList, listTab: ListTab):
        super().__init__()
        layout = QVBoxLayout()

        functionalLayout = QHBoxLayout()
        

        self.anilist = anilist
        self.listTab = listTab

        self.SearchBar = QLineEdit()
        self.SearchBar.setPlaceholderText("Search...")
        self.SearchBar.setFixedSize(QSize(1100, 40))
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
        self.SearchButton.clicked.connect(self.searchRequest)
        self.SearchButton.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                padding: 10px;
                border-radius: 4px;
                background-color: #DEE0E0;
            }
            QPushButton:hover {
                background-color: #b4b8b8;
            }
        """)
        
        functionalLayout.addWidget(self.SearchBar)
        functionalLayout.addWidget(self.SearchButton)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True) 
        self.scrollArea.setStyleSheet("""
            QScrollArea {
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background: #d3d3d3;
                width: 10px;
                border-radius: 5px;
                margin: 2px 0 2px 0;
            }
            QScrollBar::handle:vertical {
                background: #888;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #666;
            }
        """)

        self.container = QWidget()
        self.container_layout = QVBoxLayout()
        self.container_layout.setSpacing(15)
        self.container.setLayout(self.container_layout)

        self.scrollArea.setWidget(self.container)  

        self.NotFoundLabel = QLabel("No Anime Found...")
        self.NotFoundLabel.setAlignment(Qt.AlignCenter)
        self.NotFoundLabel.setStyleSheet("font-size: 30px; color: gray;")

        layout.addLayout(functionalLayout)
        layout.addWidget(self.scrollArea)  
        self.setLayout(layout)

    def searchRequest(self):
            results = searchAnime(self.SearchBar.text())

            for i in reversed(range(self.container_layout.count())):
                widget = self.container_layout.itemAt(i).widget()
                if widget is not None:
                    widget.setParent(None)

            if results:
                for anime in results:
                    card = AniSearchCard(anime)
                    # Connect the card's signal to add the anime to the list
                    card.add_signal.connect(lambda anime, a=anime: self.listTab.AddAnimeToList(a))
                    self.container_layout.addWidget(card)
            else:
                self.container_layout.addWidget(self.NotFoundLabel)
            self.container.updateGeometry()