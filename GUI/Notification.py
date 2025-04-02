from PyQt5.QtCore import QPropertyAnimation, QTimer, QPoint
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class Notification(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("""
            background-color: rgba(46, 52, 64, 220);
            color: white;
            padding: 12px 16px;
            border-radius: 8px;
            border: 1px solid #4C566A;
        """)
        
        self.label = QLabel(self)
        self.label.setFont(QFont('Segoe UI', 10))
        self.label.setStyleSheet("color: white;")
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        self.timer = QTimer()
        self.timer.timeout.connect(self.hide)

    def ShowNotification(self, text, timeout=2500):
        self.label.setText(text)
        self.adjustSize()
        
        if self.parent():
            main_window = self.parent()
            
            frame_width = 8
            title_bar_height = 30
            x = main_window.width() - self.width() - frame_width - 12  # 12px margin
            y = title_bar_height + 12  
            pos = main_window.mapToGlobal(QPoint(x, y))
            self.move(pos)
        
        self.setWindowOpacity(0) 
        self.show()
        
        self.animation.stop()
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()
        
        self.timer.start(timeout)

    def hide(self):
        self.animation.stop()
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()
        self.timer.stop()
        QTimer.singleShot(self.animation.duration(), super().hide)