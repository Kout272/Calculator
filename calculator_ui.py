from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QGridLayout, QLineEdit, QPushButton,
                             QMessageBox, QStackedWidget, QSizePolicy)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty, QTimer
from PyQt5.QtGui import QFont, QKeyEvent
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtCore import QUrl
import os
from calculator_core import CalculatorEngine
from styles import CalculatorStyles


class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self._scale = 1.0
        self.animation = QPropertyAnimation(self, b"scale")
        self.animation.setDuration(100)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)

    @pyqtProperty(float)
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        self.update()

    def mousePressEvent(self, event):
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.9)
        self.animation.start()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.animation.setStartValue(0.9)
        self.animation.setEndValue(1.0)
        self.animation.start()
        super().mouseReleaseEvent(event)


class ScientificCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_input = ""
        self.last_result = None
        self.result_displayed = False
        self.calculator_engine = CalculatorEngine()
        self.styles = CalculatorStyles()
        self.sound_effect = QSoundEffect()
        self.setup_sound()
        self.initUI()

    def setup_sound(self):
        """Настраивает звуковой эффект для кнопок"""
        try:
            # Создаем простой звуковой эффект (можно заменить на файл)
            self.sound_effect.setSource(QUrl.fromLocalFile(""))
        except:
            pass  # Если звук не доступен, продолжаем без него

    def initUI(self):
        self.setWindowTitle('Калькулятор Pro')
        self.setMinimumSize(350, 500)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Главный вертикальный layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Создаем дисплей
        self.display = self.create_display()
        main_layout.addWidget(self.display)

        # Создаем stacked widget для переключения между экранами
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Создаем основные и дополнительные экраны
        self.basic_screen = self.create_basic_screen()
        self.advanced_screen = self.create_advanced_screen()

        self.stacked_widget.addWidget(self.basic_screen)
        self.stacked_widget.addWidget(self.advanced_screen)

        # Настраиваем стили
        self.apply_styles()

        # Устанавливаем фокус на калькулятор для приема клавиатурного ввода
        self.setFocusPolicy(Qt.StrongFocus)

    def create_display(self):
        display = QLineEdit()
        display.setFont(QFont('Arial', 24))
        display.setAlignment(Qt.AlignRight)
        display.setReadOnly(False)  # Разрешаем редактирование
        display.setMaxLength(30)
        display.setMinimumHeight(70)
        display.textChanged.connect(self.on_display_text_changed)
        display.setCursorPosition(0)
        return display

    def on_display_text_changed(self):
        """Обновляет current_input при изменении текста в дисплее"""
        self.current_input = self.display.text()

    def create_basic_screen(self):
        """Создает основной экран калькулятора"""
        widget = QWidget()
        layout = QGridLayout()
        widget.setLayout(layout)
        layout.setSpacing(8)
        layout.setContentsMargins(0, 0, 0, 0)

        # Кнопки для основного экрана
        basic_buttons = [
            ('AC', 0, 0), ('%', 0, 1), ('≡', 0, 2), ('÷', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('×', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('±', 4, 0), ('0', 4, 1), ('.', 4, 2), ('=', 4, 3),
        ]

        for text, row, col in basic_buttons:
            btn = self.create_calculator_button(text)
            layout.addWidget(btn, row, col)

        return widget

    def create_advanced_screen(self):
        """Создает экран с дополнительными функциями"""
        widget = QWidget()
        layout = QGridLayout()
        widget.setLayout(layout)
        layout.setSpacing(8)
        layout.setContentsMargins(0, 0, 0, 0)

        # Дополнительные математические функции
        advanced_buttons = [
            ('π', 0, 0), ('e', 0, 1), ('(', 0, 2), (')', 0, 3),
            ('sin', 1, 0), ('cos', 1, 1), ('tan', 1, 2), ('√', 1, 3),
            ('x²', 2, 0), ('x^y', 2, 1), ('log', 2, 2), ('ln', 2, 3),
            ('⌫', 3, 0), ('C', 3, 1), ('', 3, 2), ('Назад', 3, 3),
        ]

        for text, row, col in advanced_buttons:
            if text:  # Пропускаем пустые кнопки
                btn = self.create_calculator_button(text)
                if text == 'Назад':
                    btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
                else:
                    btn.clicked.connect(lambda checked, t=text: self.on_button_click(t))
                layout.addWidget(btn, row, col)

        return widget

    def create_calculator_button(self, text):
        """Создает кнопку калькулятора с анимацией и звуком"""
        btn = AnimatedButton(text)
        btn.setFont(QFont('Arial', 16))
        btn.setMinimumSize(60, 60)
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Подключаем обработчик клика
        if text not in ['≡', 'Назад']:
            btn.clicked.connect(lambda: self.on_button_click(text))
        elif text == '≡':
            btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        # Применяем стили
        self.apply_button_style(btn, text)

        return btn

    def apply_button_style(self, btn, text):
        """Применяет стиль к кнопке в зависимости от ее типа"""
        if text in ['÷', '×', '-', '+', '=']:
            btn.setStyleSheet(self.styles.get_operator_style())
        elif text in ['AC', 'C', '⌫', '±', '%']:
            btn.setStyleSheet(self.styles.get_function_style())
        elif text == 'Назад':
            btn.setStyleSheet(self.styles.get_back_button_style())
        elif text == '≡':
            btn.setStyleSheet(self.styles.get_more_button_style())
        else:
            btn.setStyleSheet(self.styles.get_number_style())

    def apply_styles(self):
        """Применяет стили к интерфейсу"""
        self.setStyleSheet(self.styles.get_main_style())
        self.display.setStyleSheet(self.styles.get_display_style())

    def play_button_sound(self):
        """Воспроизводит звук нажатия кнопки"""
        try:
            self.sound_effect.play()
        except:
            pass  # Игнорируем ошибки воспроизведения звука

    def on_button_click(self, text):
        """Обрабатывает нажатия кнопок"""
        self.play_button_sound()

        try:
            if self.result_displayed and text not in ['C', '⌫', '±', '%']:
                # Если результат отображен и нажата не функциональная кнопка,
                # начинаем новое выражение с последнего результата
                if self.last_result is not None and text not in ['+', '-', '×', '÷']:
                    self.current_input = str(self.last_result)
                    self.display.setText(self.current_input)
                    self.result_displayed = False

            if text == '=':
                self.calculate_result()
            elif text == 'AC' or text == 'C':
                self.clear_display()
            elif text == '⌫':
                self.backspace()
            elif text == '±':
                self.toggle_sign()
            elif text == '%':
                self.calculate_percentage()
            elif text == '÷':
                self.add_character('/')
            elif text == '×':
                self.add_character('*')
            else:
                self.add_character(text)

        except Exception as e:
            self.show_error(str(e))

    def calculate_result(self):
        """Вычисляет результат выражения"""
        if self.current_input:
            try:
                result = self.calculator_engine.safe_eval(self.current_input)
                self.display.setText(str(result))
                self.current_input = str(result)
                self.last_result = result
                self.result_displayed = True
            except Exception as e:
                self.show_error(str(e))

    def calculate_percentage(self):
        """Вычисляет процент"""
        if self.current_input:
            try:
                # Если последний символ - оператор, вычисляем процент от предыдущего результата
                if self.current_input and self.current_input[-1] in ['+', '-', '*', '/']:
                    if self.last_result is not None:
                        percent_value = self.last_result * 0.01
                        self.current_input += str(percent_value)
                        self.display.setText(self.current_input)
                else:
                    # Иначе вычисляем процент от текущего числа
                    value = float(self.current_input) * 0.01
                    self.current_input = str(value)
                    self.display.setText(self.current_input)
                self.result_displayed = False
            except:
                self.show_error("Ошибка вычисления процента")

    def clear_display(self):
        """Очищает дисплей"""
        self.current_input = ""
        self.display.clear()
        self.result_displayed = False
        self.last_result = None

    def backspace(self):
        """Удаляет последний символ"""
        self.current_input = self.current_input[:-1]
        self.display.setText(self.current_input)
        self.display.setCursorPosition(len(self.current_input))
        self.result_displayed = False

    def toggle_sign(self):
        """Меняет знак числа"""
        if self.current_input:
            try:
                if self.current_input[0] == '-':
                    self.current_input = self.current_input[1:]
                else:
                    self.current_input = '-' + self.current_input
                self.display.setText(self.current_input)
                self.display.setCursorPosition(len(self.current_input))
            except:
                pass
        self.result_displayed = False

    def add_character(self, char):
        """Добавляет символ в текущий ввод"""
        # Если результат отображен и мы начинаем новое число, очищаем дисплей
        if self.result_displayed and char not in ['+', '-', '*', '/', '×', '÷']:
            self.current_input = ""
            self.result_displayed = False

        self.current_input += char
        self.display.setText(self.current_input)
        self.display.setCursorPosition(len(self.current_input))
        self.result_displayed = False

    def show_error(self, message):
        """Показывает сообщение об ошибке"""
        QMessageBox.warning(self, "Ошибка", message)
        self.clear_display()

    def keyPressEvent(self, event):
        """Обрабатывает нажатия клавиш"""
        key = event.key()
        text = event.text()

        # Обработка цифр и основных операторов
        if key in [Qt.Key_0, Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_4,
                   Qt.Key_5, Qt.Key_6, Qt.Key_7, Qt.Key_8, Qt.Key_9]:
            self.on_button_click(text)
        elif key == Qt.Key_Plus:
            self.on_button_click('+')
        elif key == Qt.Key_Minus:
            self.on_button_click('-')
        elif key == Qt.Key_Asterisk or key == Qt.Key_multiply:
            self.on_button_click('*')
        elif key == Qt.Key_Slash or key == Qt.Key_division:
            self.on_button_click('/')
        elif key == Qt.Key_Period or key == Qt.Key_Comma:
            self.on_button_click('.')
        elif key == Qt.Key_Enter or key == Qt.Key_Return or key == Qt.Key_Equal:
            self.on_button_click('=')
        elif key == Qt.Key_Backspace:
            self.on_button_click('⌫')
        elif key == Qt.Key_Escape:
            self.on_button_click('AC')
        elif key == Qt.Key_ParenLeft:
            self.on_button_click('(')
        elif key == Qt.Key_ParenRight:
            self.on_button_click(')')
        elif key == Qt.Key_Percent:
            self.on_button_click('%')
        else:
            # Для остальных символов пытаемся добавить их как текст
            if text and text.isprintable():
                self.add_character(text)

        super().keyPressEvent(event)