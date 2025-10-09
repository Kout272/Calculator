class CalculatorStyles:
    """Класс для хранения стилей калькулятора"""

    @staticmethod
    def get_main_style():
        return """
            QMainWindow {
                background-color: #000000;
                border: 1px solid #444444;
                border-radius: 15px;
            }
        """

    @staticmethod
    def get_display_style():
        return """
            QLineEdit {
                background-color: #000000;
                color: #ffffff;
                border: 2px solid #333333;
                border-radius: 10px;
                padding: 15px;
                font-size: 24px;
                selection-background-color: #444444;
            }
        """

    @staticmethod
    def get_number_style():
        return """
            QPushButton {
                background-color: #333333;
                color: #ffffff;
                border: 1px solid #444444;
                border-radius: 30px;
                font-weight: bold;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #444444;
                border: 1px solid #555555;
            }
            QPushButton:pressed {
                background-color: #555555;
            }
        """

    @staticmethod
    def get_operator_style():
        return """
            QPushButton {
                background-color: #ff9500;
                color: #ffffff;
                border: 1px solid #ff9500;
                border-radius: 30px;
                font-weight: bold;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #ffaa33;
                border: 1px solid #ffaa33;
            }
            QPushButton:pressed {
                background-color: #cc7700;
            }
        """

    @staticmethod
    def get_function_style():
        return """
            QPushButton {
                background-color: #a6a6a6;
                color: #000000;
                border: 1px solid #a6a6a6;
                border-radius: 30px;
                font-weight: bold;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #b6b6b6;
                border: 1px solid #b6b6b6;
            }
            QPushButton:pressed {
                background-color: #868686;
            }
        """

    @staticmethod
    def get_more_button_style():
        return """
            QPushButton {
                background-color: #007aff;
                color: #ffffff;
                border: 1px solid #007aff;
                border-radius: 30px;
                font-weight: bold;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #3395ff;
                border: 1px solid #3395ff;
            }
            QPushButton:pressed {
                background-color: #0056cc;
            }
        """

    @staticmethod
    def get_back_button_style():
        return """
            QPushButton {
                background-color: #ff3b30;
                color: #ffffff;
                border: 1px solid #ff3b30;
                border-radius: 30px;
                font-weight: bold;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #ff6961;
                border: 1px solid #ff6961;
            }
            QPushButton:pressed {
                background-color: #cc2f26;
            }
        """