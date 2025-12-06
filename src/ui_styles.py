class StyleSheet:
    # Colors
    BG_DARK = "#0f111a"  # Deep Blue-Grey
    BG_SIDEBAR = "#161b22"
    BG_SURFACE = "#1c2128"
    ACCENT_PRIMARY = "#00d2ff" # Neon Cyan
    ACCENT_SECONDARY = "#7d5fff" # Neon Purple
    TEXT_MAIN = "#e6edf3"
    TEXT_DIM = "#8b949e"
    
    # Global
    MAIN_WINDOW = f"""
        QMainWindow {{
            background-color: {BG_DARK};
        }}
        QScrollBar:vertical {{
            border: none; background: {BG_SIDEBAR}; width: 8px; margin: 0;
        }}
        QScrollBar::handle:vertical {{
            background: #30363d; min-height: 20px; border-radius: 4px;
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
        QMessageBox {{ background-color: {BG_SURFACE}; color: {TEXT_MAIN}; }}
        QLabel {{ color: {TEXT_MAIN}; font-family: 'Segoe UI'; }}
    """
    
    SIDEBAR = f"""
        QFrame {{
            background-color: {BG_SIDEBAR};
            border-right: 1px solid #30363d;
        }}
    """
    
    NAV_BUTTON = f"""
        QPushButton {{
            background-color: transparent;
            color: {TEXT_DIM};
            border: none;
            border-left: 3px solid transparent;
            text-align: left;
            padding-left: 30px;
            font-size: 14px;
            font-weight: 500;
        }}
        QPushButton:hover {{
            background-color: rgba(255, 255, 255, 0.05);
            color: {TEXT_MAIN};
        }}
        QPushButton:checked {{
            color: {ACCENT_PRIMARY};
            border-left: 3px solid {ACCENT_PRIMARY};
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 210, 255, 0.1), stop:1 transparent);
        }}
    """
    
    INPUT_FIELD = f"""
        QLineEdit {{
            background-color: {BG_SURFACE};
            border: 1px solid #30363d;
            border-radius: 6px;
            color: {TEXT_MAIN};
            padding: 10px;
            font-size: 13px;
        }}
        QLineEdit:focus {{
            border: 1px solid {ACCENT_PRIMARY};
        }}
    """
    
    COMBO_BOX = f"""
        QComboBox {{
            background-color: {BG_SURFACE};
            border: 1px solid #30363d;
            border-radius: 6px;
            color: {TEXT_MAIN};
            padding: 5px 10px;
        }}
    """
    
    CONSOLE = f"""
        QTextEdit {{
            background-color: #0d1117;
            border: 1px solid #30363d;
            border-radius: 8px;
            color: #58a6ff;
            font-family: 'Consolas', 'Courier New';
            font-size: 11px;
            padding: 10px;
        }}
    """
