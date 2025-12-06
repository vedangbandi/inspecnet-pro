from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QIcon, QColor, QPainter

class StatusPill(QLabel):
    def __init__(self, text="READY"):
        super().__init__(text)
        self.setAlignment(Qt.AlignCenter)
        self.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self.setFixedSize(120, 30)
        self.set_status("NEUTRAL")

    def set_status(self, mode):
        if mode == "GOOD":
            self.setStyleSheet("background-color: rgba(46, 204, 113, 0.15); color: #2ecc71; border: 1px solid #2ecc71; border-radius: 14px;")
        elif mode == "WARN":
            self.setStyleSheet("background-color: rgba(241, 196, 15, 0.15); color: #f1c40f; border: 1px solid #f1c40f; border-radius: 14px;")
        elif mode == "DANGER":
            self.setStyleSheet("background-color: rgba(231, 76, 60, 0.15); color: #e74c3c; border: 1px solid #e74c3c; border-radius: 14px;")
        else:
            self.setStyleSheet("background-color: rgba(255, 255, 255, 0.05); color: #8b949e; border: 1px solid #30363d; border-radius: 14px;")

class KPICard(QFrame):
    def __init__(self, title, value, icon=""):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: #1c2128;
                border: 1px solid #30363d;
                border-radius: 12px;
            }
            QFrame:hover {
                border: 1px solid #00d2ff;
                background-color: #21262d;
            }
        """)
        self.setFixedSize(160, 110)
        
        # Shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 5)
        self.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15,15,15,15)
        
        t_lbl = QLabel(title.upper())
        t_lbl.setStyleSheet("color: #8b949e; font-size: 10px; font-weight: bold; border: none; background: transparent;")
        
        self.v_lbl = QLabel(value)
        self.v_lbl.setStyleSheet("color: #e6edf3; font-size: 26px; font-weight: bold; border: none; background: transparent;")
        
        layout.addWidget(t_lbl)
        layout.addWidget(self.v_lbl)
        
    def update_value(self, val):
        self.v_lbl.setText(str(val))

class PremiumButton(QPushButton):
    def __init__(self, text, icon=None, primary=True):
        super().__init__(text)
        self.setFixedHeight(45)
        self.setCursor(Qt.PointingHandCursor)
        
        base_style = """
            QPushButton {
                border-radius: 6px;
                font-family: 'Segoe UI';
                font-weight: 600;
                font-size: 13px;
                padding: 0 20px;
            }
        """
        
        if primary:
            self.setStyleSheet(base_style + """
                QPushButton {
                    background-color: #00d2ff;
                    color: #000;
                    border: none;
                }
                QPushButton:hover { background-color: #33dbff; }
                QPushButton:pressed { background-color: #0091b9; padding-top: 2px; }
            """)
        else:
            self.setStyleSheet(base_style + """
                QPushButton {
                    background-color: transparent;
                    border: 1px solid #30363d;
                    color: #e6edf3;
                }
                QPushButton:hover { border-color: #00d2ff; color: #00d2ff; background: rgba(0, 210, 255, 0.05); }
            """)
