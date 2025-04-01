from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QFrame, QPushButton,QMessageBox
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QSize, pyqtSignal

from Entities.Anime import Anime
from Entities.State import State
from DataFetch.ImageFetch import GetImage

class NoScrollComboBox(QComboBox):
    def __init__(self):
        super().__init__()
    
    def wheelEvent(self, e):
        e.ignore()


class AniCard(QFrame):
    remove_signal = pyqtSignal(object)
    def __init__(self, anime: Anime):
        super().__init__()
        self.setFixedSize(600,350)
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
        } QPushButton#CloseButton {
            background-color: #DEE0E0;
            color: white;
            border-radius: 10px;
            font-size: 14px;
        } QPushButton#CloseButton:hover {
            background-color: #611c15;
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

        TitleLabel = QLabel(f"{anime.Title}")
        TitleLabel.setWordWrap(True)
        TitleLabel.setFont(font)
        TitleLabel.setFixedWidth(250)
        EpLabel = QLabel(f"{anime.NumberEp} episodes")
        EpLabel.setFont(font)
        EpLabel.setFixedWidth(250)
        StatusLabel = QLabel(f"{anime.Status.capitalize()}")
        StatusLabel.setFont(font)
        StatusLabel.setFixedWidth(250)
        CurrentStateLabel = NoScrollComboBox()
        CurrentStateLabel.setFont(font)
        for state in State:
            CurrentStateLabel.addItem(state.name)
        
        self.close_button = QPushButton("X")
        self.close_button.setFixedSize(30, 30)
        closeFont = font
        closeFont.setBold(True)
        self.close_button.setFont(closeFont)
        self.close_button.setObjectName("CloseButton")
        self.close_button.clicked.connect(self.__RemoveAnime)

        InfoLayout.addWidget(self.close_button, alignment=Qt.AlignRight)
        InfoLayout.addWidget(TitleLabel)
        InfoLayout.addWidget(EpLabel)
        InfoLayout.addWidget(StatusLabel)
        InfoLayout.addWidget(CurrentStateLabel)

        layout.addLayout(InfoLayout)
        self.setLayout(layout)

    def __RemoveAnime(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Delete Confirmation")
        msg_box.setText(f"Are you sure you want to remove this anime from your list?")
        msg_box.setIcon(QMessageBox.Warning)
        yes_button = msg_box.addButton("Yes", QMessageBox.YesRole)
        no_button = msg_box.addButton("No", QMessageBox.NoRole)
        msg_box.exec_()
        
        if msg_box.clickedButton() == yes_button:
            self.remove_signal.emit(self)