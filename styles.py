class CalculatorStyles:
    """Класс для хранения стилей калькулятора"""

    @staticmethod
    def get_main_style():
        return """
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #0a0a0a, stop:0.3 #1a1a2e, stop:0.7 #16213e, stop:1 #0f3460);
                border: 2px solid #2d3748;
                border-radius: 20px;
            }
            
            QTabWidget::pane {
                border: 2px solid #2d3748;
                border-radius: 15px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #1a1a2e, stop:1 #16213e);
            }
            
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #2d3748, stop:1 #4a5568);
                color: #e2e8f0;
                border: 1px solid #4a5568;
                border-radius: 10px;
                padding: 15px 30px;
                margin: 3px;
                font-size: 16px;
                font-weight: bold;
                min-width: 120px;
                min-height: 45px;
            }
            
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #667eea, stop:1 #764ba2);
                color: #ffffff;
                border: 2px solid #667eea;
                min-width: 120px;
                min-height: 45px;
            }
            
            QTabBar::tab:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #4a5568, stop:1 #718096);
                min-width: 120px;
                min-height: 45px;
            }
            
            QLabel {
                color: #e2e8f0;
                font-size: 16px;
                font-weight: bold;
            }
            
            QLineEdit {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #2d3748, stop:1 #4a5568);
                color: #ffffff;
                border: 2px solid #4a5568;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }
            
            QLineEdit:focus {
                border: 2px solid #667eea;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #4a5568, stop:1 #718096);
            }
            
            QComboBox {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #2d3748, stop:1 #4a5568);
                color: #ffffff;
                border: 2px solid #4a5568;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
            }
            
            QComboBox:focus {
                border: 2px solid #667eea;
            }
            
            QComboBox::drop-down {
                border: none;
                background: transparent;
            }
            
            QComboBox::down-arrow {
                image: none;
                border: 2px solid #e2e8f0;
                width: 8px;
                height: 8px;
                border-top: none;
                border-right: none;
                transform: rotate(-45deg);
            }
            
            QTextEdit {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #2d3748, stop:1 #4a5568);
                color: #e2e8f0;
                border: 2px solid #4a5568;
                border-radius: 10px;
                padding: 15px;
                font-size: 14px;
                selection-background-color: #667eea;
                selection-color: #ffffff;
            }
            
            QTextEdit:focus {
                border: 2px solid #667eea;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #4a5568, stop:1 #718096);
            }
            
            QScrollArea {
                background: transparent;
                border: none;
            }
            
            QScrollBar:vertical {
                background: #2d3748;
                width: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:vertical {
                background: #667eea;
                border-radius: 6px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: #764ba2;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            
            /* Стили для диалоговых окон */
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #f7fafc, stop:1 #edf2f7);
                color: #2d3748;
            }
            
            QInputDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #f7fafc, stop:1 #edf2f7);
                color: #2d3748;
            }
            
            QMessageBox {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #f7fafc, stop:1 #edf2f7);
                color: #2d3748;
            }
            
            QDialog QLabel {
                color: #2d3748;
                font-size: 14px;
                font-weight: bold;
            }
            
            QInputDialog QLabel {
                color: #2d3748;
                font-size: 14px;
                font-weight: bold;
            }
            
            QMessageBox QLabel {
                color: #2d3748;
                font-size: 14px;
                font-weight: bold;
            }
            
            QDialog QLineEdit {
                background: #ffffff;
                color: #2d3748;
                border: 2px solid #cbd5e0;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
            }
            
            QInputDialog QLineEdit {
                background: #ffffff;
                color: #2d3748;
                border: 2px solid #cbd5e0;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
            }
            
            QDialog QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #667eea, stop:1 #764ba2);
                color: #ffffff;
                border: 2px solid #667eea;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
                min-width: 80px;
                min-height: 30px;
            }
            
            QDialog QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #8b9cff, stop:1 #9c88ff);
                border: 2px solid #8b9cff;
            }
            
            QDialog QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #5a67d8, stop:1 #553c9a);
                border: 2px solid #5a67d8;
            }
        """

    @staticmethod
    def get_display_style():
        return """
            QTextEdit {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #1a1a2e, stop:0.5 #16213e, stop:1 #0f3460);
                color: #ffffff;
                border: 3px solid #667eea;
                border-radius: 15px;
                padding: 25px;
                font-size: 32px;
                font-weight: bold;
                selection-background-color: #667eea;
                selection-color: #ffffff;
            }
            
            QTextEdit:focus {
                border: 3px solid #764ba2;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #16213e, stop:0.5 #0f3460, stop:1 #1a1a2e);
            }
        """

    @staticmethod
    def get_number_style():
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #4a5568, stop:0.5 #2d3748, stop:1 #1a202c);
                color: #ffffff;
                border: 2px solid #4a5568;
                border-radius: 35px;
                font-weight: bold;
                font-size: 20px;
                min-height: 60px;
                min-width: 60px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #667eea, stop:0.5 #764ba2, stop:1 #667eea);
                border: 2px solid #667eea;
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #5a67d8, stop:0.5 #553c9a, stop:1 #5a67d8);
                border: 2px solid #5a67d8;
                transform: scale(0.95);
            }
        """

    @staticmethod
    def get_operator_style():
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #ff6b6b, stop:0.5 #ee5a24, stop:1 #ff6b6b);
                color: #ffffff;
                border: 2px solid #ff6b6b;
                border-radius: 35px;
                font-weight: bold;
                font-size: 20px;
                min-height: 60px;
                min-width: 60px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #ff8e8e, stop:0.5 #ff7675, stop:1 #ff8e8e);
                border: 2px solid #ff8e8e;
                transform: scale(1.05);
                box-shadow: 0 0 20px rgba(255, 107, 107, 0.5);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #ff5252, stop:0.5 #e74c3c, stop:1 #ff5252);
                border: 2px solid #ff5252;
                transform: scale(0.95);
            }
        """

    @staticmethod
    def get_function_style():
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #718096, stop:0.5 #4a5568, stop:1 #2d3748);
                color: #ffffff;
                border: 2px solid #718096;
                border-radius: 35px;
                font-weight: bold;
                font-size: 20px;
                min-height: 60px;
                min-width: 60px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #a0aec0, stop:0.5 #718096, stop:1 #a0aec0);
                border: 2px solid #a0aec0;
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #4a5568, stop:0.5 #2d3748, stop:1 #4a5568);
                border: 2px solid #4a5568;
                transform: scale(0.95);
            }
        """

    @staticmethod
    def get_more_button_style():
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #667eea, stop:0.5 #764ba2, stop:1 #667eea);
                color: #ffffff;
                border: 2px solid #667eea;
                border-radius: 35px;
                font-weight: bold;
                font-size: 20px;
                min-height: 60px;
                min-width: 60px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #8b9cff, stop:0.5 #9c88ff, stop:1 #8b9cff);
                border: 2px solid #8b9cff;
                transform: scale(1.05);
                box-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #5a67d8, stop:0.5 #553c9a, stop:1 #5a67d8);
                border: 2px solid #5a67d8;
                transform: scale(0.95);
            }
        """

    @staticmethod
    def get_back_button_style():
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #f56565, stop:0.5 #e53e3e, stop:1 #f56565);
                color: #ffffff;
                border: 2px solid #f56565;
                border-radius: 35px;
                font-weight: bold;
                font-size: 20px;
                min-height: 60px;
                min-width: 60px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #fc8181, stop:0.5 #f56565, stop:1 #fc8181);
                border: 2px solid #fc8181;
                transform: scale(1.05);
                box-shadow: 0 0 20px rgba(245, 101, 101, 0.5);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #e53e3e, stop:0.5 #c53030, stop:1 #e53e3e);
                border: 2px solid #e53e3e;
                transform: scale(0.95);
            }
        """

    @staticmethod
    def get_rainbow_number_style(color):
        """Возвращает стиль для цифр с радужными цветами"""
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 {color}, stop:0.5 {color}dd, stop:1 {color});
                color: #ffffff;
                border: 2px solid {color};
                border-radius: 35px;
                font-weight: bold;
                font-size: 20px;
                min-height: 60px;
                min-width: 60px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 {color}ff, stop:0.5 {color}, stop:1 {color}ff);
                border: 2px solid {color}ff;
                transform: scale(1.05);
                box-shadow: 0 0 20px {color}80;
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 {color}cc, stop:0.5 {color}aa, stop:1 {color}cc);
                border: 2px solid {color}cc;
                transform: scale(0.95);
            }}
        """

    @staticmethod
    def get_rainbow_operator_style(color):
        """Возвращает стиль для операторов с радужными цветами"""
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 {color}, stop:0.5 {color}dd, stop:1 {color});
                color: #ffffff;
                border: 2px solid {color};
                border-radius: 35px;
                font-weight: bold;
                font-size: 20px;
                min-height: 60px;
                min-width: 60px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 {color}ff, stop:0.5 {color}, stop:1 {color}ff);
                border: 2px solid {color}ff;
                transform: scale(1.05);
                box-shadow: 0 0 20px {color}80;
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 {color}cc, stop:0.5 {color}aa, stop:1 {color}cc);
                border: 2px solid {color}cc;
                transform: scale(0.95);
            }}
        """

    @staticmethod
    def get_help_button_style():
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #48bb78, stop:0.5 #38a169, stop:1 #48bb78);
                color: #ffffff;
                border: 2px solid #48bb78;
                border-radius: 35px;
                font-weight: bold;
                font-size: 20px;
                min-height: 60px;
                min-width: 60px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #68d391, stop:0.5 #48bb78, stop:1 #68d391);
                border: 2px solid #68d391;
                transform: scale(1.05);
                box-shadow: 0 0 20px rgba(72, 187, 120, 0.5);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #38a169, stop:0.5 #2f855a, stop:1 #38a169);
                border: 2px solid #38a169;
                transform: scale(0.95);
            }
        """

    @staticmethod
    def get_financial_button_style():
        """Стиль для финансовых кнопок"""
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #f6ad55, stop:0.5 #ed8936, stop:1 #f6ad55);
                color: #ffffff;
                border: 2px solid #f6ad55;
                border-radius: 25px;
                font-weight: bold;
                font-size: 16px;
                min-height: 50px;
                min-width: 120px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #fbb6ce, stop:0.5 #f6ad55, stop:1 #fbb6ce);
                border: 2px solid #fbb6ce;
                transform: scale(1.02);
                box-shadow: 0 0 15px rgba(246, 173, 85, 0.4);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #ed8936, stop:0.5 #dd6b20, stop:1 #ed8936);
                border: 2px solid #ed8936;
                transform: scale(0.98);
            }
        """

    @staticmethod
    def get_currency_button_style():
        """Стиль для кнопок конвертации валют"""
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #9f7aea, stop:0.5 #805ad5, stop:1 #9f7aea);
                color: #ffffff;
                border: 2px solid #9f7aea;
                border-radius: 25px;
                font-weight: bold;
                font-size: 16px;
                min-height: 50px;
                min-width: 140px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #b794f6, stop:0.5 #9f7aea, stop:1 #b794f6);
                border: 2px solid #b794f6;
                transform: scale(1.02);
                box-shadow: 0 0 15px rgba(159, 122, 234, 0.4);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #805ad5, stop:0.5 #6b46c1, stop:1 #805ad5);
                border: 2px solid #805ad5;
                transform: scale(0.98);
            }
        """