import sys
import time
import threading
import ctypes

from pypresence import Presence
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPixmap

from GUI.ListTab import ListTab
from GUI.SearchTab import SearchTab
from Utilities.ClinetIdGetter import GetClientID
from Storage.StorageManager import StorageMan
from Storage.AniList import AniList

CLIENT_ID = GetClientID()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('AniWatchList')
        self.setWindowIcon(QIcon(QPixmap('Utilities/logo.png')))
        self.setFixedSize(QSize(1300, 800))

        if sys.platform.startswith("win"):
            app_id = "AniWatchList"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

        self.StoreMan = StorageMan()
        self.anilis = AniList()
        self.StoreMan.LoadList(aniList=self.anilis)

        # Setup Tabs
        self.tabs = QTabWidget()
        self.listTab = ListTab(self.anilis, self.StoreMan)
        self.searchTab = SearchTab(self.anilis, self.listTab)        
        self.tabs.addTab(self.listTab, "My List")
        self.tabs.addTab(self.searchTab, "Search")
        self.tabs.currentChanged.connect(self.update_presence)
        self.tabs.setStyleSheet("""
        QTabWidget::pane {
            border: 1px solid #ccc;
            background: #f0f0f0;
        } 
        QTabBar::tab {
            background: #d3d3d3;
            border: 1px solid #ccc;
            padding: 8px 12px;
            font-size: 14px;
            color: #333;
            min-width: 100px;
        } 
        QTabBar::tab:selected {
            background: #DEE0E0;
            color: #000;
        } 
        QTabBar::tab:hover {
            background: #e0e0e0;
        }
        """)

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

        self.rpc = None
        self.rpc_thread = threading.Thread(target=self.start_rpc, daemon=True)
        self.rpc_thread.start()

    def start_rpc(self):
        """Simplified Discord RPC connection without asyncio"""
        try:
            self.rpc = Presence(CLIENT_ID)
            self.rpc.connect()
            self.update_presence()
            
            while True:
                time.sleep(15) 
                self.update_presence()
        except Exception as e:
            print(f"Discord RPC Error: {e}")
        finally:
            if hasattr(self, 'rpc') and self.rpc:
                try:
                    self.rpc.close()
                except:
                    pass

    def update_presence(self):
        if not self.rpc:
            return  

        tab_index = self.tabs.currentIndex()
        state_text = "Browsing Anime List" if tab_index == 0 else "Searching for Anime"
        details_text = "Exploring the watchlist" if tab_index == 0 else "Looking up new titles"

        try:
            self.rpc.update(
                state=state_text,
                details=details_text,
                large_image="logo",
                large_text="AniWatchList",
                start=int(time.time())
            )
        except Exception as e:
            print(f"Failed to update presence: {e}")

    def closeEvent(self, event):
        """Cleanup on window close"""
        if hasattr(self, 'rpc') and self.rpc:
            try:
                self.rpc.close()
            except Exception as e:
                print(f"RPC close error: {e}")
        event.accept()

def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run()