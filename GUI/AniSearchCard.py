from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QFrame, QPushButton
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QSize, pyqtSignal

from Entities.Anime import Anime
from Entities.State import State
from DataFetch.ImageFetch import GetImage
from GUI.AniCard import NoScrollComboBox


class AniSearchCard(QFrame):
    add_signal = pyqtSignal(object)
    def __init__(self, anime: Anime):
        super().__init__()
        self.setFixedSize(QSize(1000,350))
        self.anime = anime

        self.setStyleSheet("""
        QFrame {
            background-color: #FFFFFF;
            border-radius: 10px;
        } QLabel {
            background-color: #DEE0E0;
            border-radius: 10px;
            padding: 8px;
        } QLabel#ImageLabel {
            background-color: #FFFFFF;
            border-radius: 0px;
            padding: 0px;
        } QComboBox {
            background-color: #DEE0E0;
            border-radius: 8px;       
            padding: 6px 12px;        
            selection-background-color: #444444;
        } QComboBox:hover {
            border: 2px solid #888888;
        } QComboBox::drop-down {
            border: none;             
            width: 20px;              
        } QComboBox QAbstractItemView {
            background-color: #DEE0E0;
            border-radius: 6px;
            border: 1px solid #555555;
            selection-background-color: #444444;
            padding: 4px;
        } QComboBox QAbstractItemView::item {
            padding: 6px 12px;
        } QComboBox QAbstractItemView::item:selected {
            background-color: #555555;
            color: #FFFFFF;
            border-radius: 4px;
        } QPushButton {
            border-radius: 4px;
            color: #61b02c;
            background-color: #DEE0E0;
        } QPushButton::hover {
            color: #427023;
        }
        """)

        layout = QHBoxLayout(self)
        font = QFont('Arial', 16)

        #Image Label and Content is stored in the main layout
        CoverImageLabel = QLabel(self)
        CoverImageLabel.setObjectName("ImageLabel")
        CoverImage = QPixmap(GetImage(anime=anime))
        CoverImageLabel.setPixmap(CoverImage)
        CoverImageLabel.setFixedSize(QSize(230, 320))
        layout.addWidget(CoverImageLabel)

        #Information section is stored in this layout
        InfoLayout = QVBoxLayout()
        InfoLayout.setAlignment(Qt.AlignCenter) 
        InfoLayout.setSpacing(30) 

        # TitleLabel = QLabel(f"{anime.Title}")
        # TitleLabel.setWordWrap(True)
        # TitleLabel.setFont(font)
        # TitleLabel.setFixedWidth(250)
        # EpLabel = QLabel(f"{anime.NumberEp} episodes")
        # EpLabel.setFont(font)
        # EpLabel.setFixedWidth(250)
        # StatusLabel = QLabel(f"{anime.Status.capitalize()}")
        # StatusLabel.setFont(font)
        # StatusLabel.setFixedWidth(250)

        InfoLabel = QLabel()
        InfoLabel.setText(f"<br>{anime.Title}<br><br>{anime.NumberEp or 0} episodes<br><br>{anime.Status.capitalize().replace('_',' ')}<br><br>{anime.AniType or 'Unknown'}<br>")
        InfoLabel.setWordWrap(True)
        InfoLabel.setFont(font)
        InfoLabel.setFixedWidth(400)

        SecondaryLayout = QVBoxLayout()
        genres: list[str] = [genre for genre in anime.Genres]
        GenreText = "\n"
        for i in range(len(genres)):
            txt = (genres[i].capitalize() + '\n')
            if i != len(genres)-1:
                txt += '\n'
            GenreText += txt
        GenreLabel = QLabel(f"{GenreText}")
        GenreLabel.setFont(font)

        self.addAnimeButton = QPushButton("+")
        self.addAnimeButton.clicked.connect(self.addAnime)
        addFont = QFont('Arial', 24)
        addFont.bold()
        self.addAnimeButton.setFont(addFont)

        SecondaryLayout.setAlignment(Qt.AlignCenter) 
        SecondaryLayout.addWidget(GenreLabel)
        SecondaryLayout.addWidget(self.addAnimeButton)

        CurrentStateLabel = NoScrollComboBox()
        CurrentStateLabel.setFont(font)
        for state in State:
            CurrentStateLabel.addItem(state.name)

        # InfoLayout.addWidget(TitleLabel)
        # InfoLayout.addWidget(EpLabel)
        # InfoLayout.addWidget(StatusLabel)
        InfoLayout.addWidget(InfoLabel)
        InfoLayout.addWidget(CurrentStateLabel)

        layout.addLayout(InfoLayout)
        layout.addLayout(SecondaryLayout)
        self.setLayout(layout)
    
    def addAnime(self):
        self.add_signal.emit(self.anime)