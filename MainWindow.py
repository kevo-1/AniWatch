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

CLIENT_ID = GetClientID()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('AniWatchList')
        self.setWindowIcon(QIcon(QPixmap('D:/Projects/AniWatch/Utilities/logo.png')))
        self.setFixedSize(QSize(1500, 800))

        if sys.platform.startswith("win"):
            app_id = "AniWatchList"  # Unique app ID
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

        # Setup Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(ListTab(), "Anime List")
        self.tabs.addTab(SearchTab(), "Search Anime")
        self.tabs.currentChanged.connect(self.update_presence)

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

        # Start Discord Presence in a separate thread
        self.rpc = None
        self.rpc_thread = threading.Thread(target=self.start_rpc, daemon=True)
        self.rpc_thread.start()

    def start_rpc(self):
        """Starts Discord Rich Presence in a separate thread."""
        try:
            self.rpc = Presence(CLIENT_ID)
            self.rpc.connect()
            self.update_presence()  # Update presence once connected
        except Exception as e:
            print(f"Discord RPC Error: {e}")

    def update_presence(self):
        """Update Discord Rich Presence based on the active tab."""
        if not self.rpc:
            return  # If RPC failed to connect, do nothing

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
        """Clear Discord Rich Presence on exit."""
        if self.rpc:
            try:
                self.rpc.clear()
                self.rpc.close()
            except Exception as e:
                print(f"Failed to close RPC: {e}")
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
