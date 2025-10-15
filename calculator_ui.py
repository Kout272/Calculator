from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QGridLayout, QLineEdit, QPushButton,
                             QMessageBox, QStackedWidget, QSizePolicy, QTextEdit,
                             QTabWidget, QHBoxLayout, QLabel, QScrollArea, QInputDialog,
                             QComboBox, QGroupBox, QCheckBox, QListWidget, QListWidgetItem)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty, QTimer
from PyQt5.QtGui import QFont, QKeyEvent
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtCore import QUrl
import os
try:
    import requests
    import json
    from datetime import datetime, timedelta
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("Библиотека requests не установлена. Используем встроенные курсы валют.")
    # Встроенные курсы валют как fallback
    FALLBACK_RATES = {
        "USD": {"BYN": 3.2, "EUR": 0.85, "RUB": 95.0, "UAH": 36.5, "PLN": 4.0, "GBP": 0.79, "CHF": 0.88, "JPY": 150.0, "CNY": 7.2, "CAD": 1.35, "AUD": 1.52},
        "EUR": {"BYN": 3.76, "USD": 1.18, "RUB": 111.8, "UAH": 42.9, "PLN": 4.7, "GBP": 0.93, "CHF": 1.04, "JPY": 176.5, "CNY": 8.47, "CAD": 1.59, "AUD": 1.79},
        "BYN": {"USD": 0.31, "EUR": 0.27, "RUB": 29.7, "UAH": 11.4, "PLN": 1.25, "GBP": 0.25, "CHF": 0.28, "JPY": 46.9, "CNY": 2.25, "CAD": 0.42, "AUD": 0.48},
        "RUB": {"USD": 0.011, "EUR": 0.009, "BYN": 0.034, "UAH": 0.38, "PLN": 0.042, "GBP": 0.008, "CHF": 0.009, "JPY": 1.58, "CNY": 0.076, "CAD": 0.014, "AUD": 0.016},
        "UAH": {"USD": 0.027, "EUR": 0.023, "BYN": 0.088, "RUB": 2.63, "PLN": 0.11, "GBP": 0.022, "CHF": 0.024, "JPY": 4.11, "CNY": 0.20, "CAD": 0.037, "AUD": 0.042},
        "PLN": {"USD": 0.25, "EUR": 0.21, "BYN": 0.80, "RUB": 23.8, "UAH": 9.09, "GBP": 0.20, "CHF": 0.22, "JPY": 37.5, "CNY": 1.80, "CAD": 0.34, "AUD": 0.38},
        "GBP": {"USD": 1.27, "EUR": 1.08, "BYN": 4.0, "RUB": 120.0, "UAH": 45.6, "PLN": 5.0, "CHF": 1.11, "JPY": 190.0, "CNY": 9.1, "CAD": 1.71, "AUD": 1.93},
        "CHF": {"USD": 1.14, "EUR": 0.96, "BYN": 3.6, "RUB": 108.0, "UAH": 41.0, "PLN": 4.5, "GBP": 0.90, "JPY": 170.0, "CNY": 8.2, "CAD": 1.54, "AUD": 1.73},
        "JPY": {"USD": 0.0067, "EUR": 0.0057, "BYN": 0.021, "RUB": 0.63, "UAH": 0.24, "PLN": 0.027, "GBP": 0.0053, "CHF": 0.0059, "CNY": 0.048, "CAD": 0.009, "AUD": 0.010},
        "CNY": {"USD": 0.14, "EUR": 0.12, "BYN": 0.44, "RUB": 13.2, "UAH": 5.0, "PLN": 0.56, "GBP": 0.11, "CHF": 0.12, "JPY": 20.8, "CAD": 0.19, "AUD": 0.21},
        "CAD": {"USD": 0.74, "EUR": 0.63, "BYN": 2.4, "RUB": 71.4, "UAH": 27.0, "PLN": 2.9, "GBP": 0.58, "CHF": 0.65, "JPY": 111.0, "CNY": 5.3, "AUD": 1.13},
        "AUD": {"USD": 0.66, "EUR": 0.56, "BYN": 2.1, "RUB": 63.0, "UAH": 24.0, "PLN": 2.6, "GBP": 0.52, "CHF": 0.58, "JPY": 98.0, "CNY": 4.7, "CAD": 0.88}
    }
from calculator_core import CalculatorEngine, StepByStepSolver
from styles import CalculatorStyles


class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self._scale = 1.0
        self._glow = 0.0
        
        # Анимация масштабирования
        self.scale_animation = QPropertyAnimation(self, b"scale")
        self.scale_animation.setDuration(150)
        self.scale_animation.setEasingCurve(QEasingCurve.OutBack)
        
        # Анимация свечения
        self.glow_animation = QPropertyAnimation(self, b"glow")
        self.glow_animation.setDuration(200)
        self.glow_animation.setEasingCurve(QEasingCurve.OutQuart)
        
        # Таймер для автоматического сброса свечения
        self.glow_timer = QTimer()
        self.glow_timer.setSingleShot(True)
        self.glow_timer.timeout.connect(self.reset_glow)

    @pyqtProperty(float)
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        self.update()

    @pyqtProperty(float)
    def glow(self):
        return self._glow

    @glow.setter
    def glow(self, value):
        self._glow = value
        self.update()

    def mousePressEvent(self, event):
        # Анимация нажатия
        self.scale_animation.setStartValue(1.0)
        self.scale_animation.setEndValue(0.85)
        self.scale_animation.start()
        
        # Эффект свечения
        self.glow_animation.setStartValue(0.0)
        self.glow_animation.setEndValue(1.0)
        self.glow_animation.start()
        
        # Сброс свечения через 300мс
        self.glow_timer.start(300)
        
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        # Возврат к нормальному размеру
        self.scale_animation.setStartValue(0.85)
        self.scale_animation.setEndValue(1.0)
        self.scale_animation.start()
        
        super().mouseReleaseEvent(event)

    def enterEvent(self, event):
        # Эффект при наведении
        self.scale_animation.setStartValue(1.0)
        self.scale_animation.setEndValue(1.05)
        self.scale_animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        # Возврат к нормальному размеру при уходе курсора
        self.scale_animation.setStartValue(1.05)
        self.scale_animation.setEndValue(1.0)
        self.scale_animation.start()
        super().leaveEvent(event)

    def reset_glow(self):
        """Сбрасывает эффект свечения"""
        self.glow_animation.setStartValue(1.0)
        self.glow_animation.setEndValue(0.0)
        self.glow_animation.start()

    def paintEvent(self, event):
        """Переопределяем отрисовку для добавления эффектов"""
        from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
        from PyQt5.QtCore import QRect
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Получаем размеры кнопки
        rect = self.rect()
        
        # Применяем масштабирование
        if self._scale != 1.0:
            center = rect.center()
            painter.translate(center)
            painter.scale(self._scale, self._scale)
            painter.translate(-center)
        
        # Эффект свечения
        if self._glow > 0:
            glow_pen = QPen(QColor(255, 255, 255, int(100 * self._glow)))
            glow_pen.setWidth(int(8 * self._glow))
            painter.setPen(glow_pen)
            painter.setBrush(QBrush())
            painter.drawRoundedRect(rect.adjusted(4, 4, -4, -4), 35, 35)
        
        # Вызываем стандартную отрисовку
        super().paintEvent(event)


class MultiCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_input = ""
        self.last_result = None
        self.result_displayed = False
        self.calculator_engine = CalculatorEngine()
        self.step_solver = StepByStepSolver()
        self.styles = CalculatorStyles()
        self.sound_effect = QSoundEffect()
        self.currency_rates = {}  # Кэш курсов валют
        self.last_currency_update = None
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
        self.setWindowTitle('Мульти-Калькулятор Pro')
        self.setMinimumSize(900, 700)
        self.resize(1000, 750)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Главный вертикальный layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Создаем вкладки
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # Создаем окна
        self.basic_calc = self.create_basic_calculator()
        self.scientific_calc = self.create_scientific_calculator()
        self.programmer_calc = self.create_programmer_tab()
        self.graph_calc = self.create_graph_tab()
        self.financial_calc = self.create_financial_calculator()
        self.notes_window = self.create_notes_window()

        # Добавляем вкладки (Заметки последней)
        self.tab_widget.addTab(self.basic_calc, "📱 Стандартный")
        self.tab_widget.addTab(self.scientific_calc, "🔬 Научный")
        self.tab_widget.addTab(self.programmer_calc, "🧮 Программист")
        self.tab_widget.addTab(self.graph_calc, "📈 График")
        self.tab_widget.addTab(self.financial_calc, "💰 Финансы")
        self.tab_widget.addTab(self.notes_window, "📝 Заметки")

        # Настраиваем стили
        self.apply_styles()

        # Устанавливаем фокус на калькулятор для приема клавиатурного ввода
        self.setFocusPolicy(Qt.StrongFocus)

    def create_programmer_tab(self):
        """Создает вкладку режима программиста (скроллинг и разреженная компоновка)"""
        widget = QWidget()
        main_layout = QVBoxLayout(); widget.setLayout(main_layout)
        main_layout.setContentsMargins(0,0,0,0)

        # Скролл-область
        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        main_layout.addWidget(scroll)
        content = QWidget(); scroll.setWidget(content)
        layout = QVBoxLayout(content)
        layout.setSpacing(16)
        layout.setContentsMargins(6, 6, 6, 12)

        # Верх: ввод числа и выбор системы счисления
        top = QHBoxLayout()
        layout.addLayout(top)

        self.prog_input = QLineEdit()
        self.prog_input.setPlaceholderText("Введите число (например, FF или 1011)")
        top.addWidget(self.prog_input, 3)

        self.prog_base = QComboBox()
        self.prog_base.addItems(["BIN", "OCT", "DEC", "HEX"])
        self.prog_base.setCurrentText("DEC")
        top.addWidget(self.prog_base, 1)

        convert_btn = AnimatedButton("Перевести")
        convert_btn.clicked.connect(self.prog_convert)
        convert_btn.setStyleSheet(self.styles.get_function_style())
        top.addWidget(convert_btn, 1)

        # Средняя панель: результаты конвертации
        grid = QGridLayout(); grid.setHorizontalSpacing(12); grid.setVerticalSpacing(8)
        layout.addLayout(grid)

        self.out_bin = QLineEdit(); self.out_bin.setReadOnly(True)
        self.out_oct = QLineEdit(); self.out_oct.setReadOnly(True)
        self.out_dec = QLineEdit(); self.out_dec.setReadOnly(True)
        self.out_hex = QLineEdit(); self.out_hex.setReadOnly(True)

        grid.addWidget(QLabel("BIN"), 0, 0); grid.addWidget(self.out_bin, 0, 1)
        grid.addWidget(QLabel("OCT"), 1, 0); grid.addWidget(self.out_oct, 1, 1)
        grid.addWidget(QLabel("DEC"), 2, 0); grid.addWidget(self.out_dec, 2, 1)
        grid.addWidget(QLabel("HEX"), 3, 0); grid.addWidget(self.out_hex, 3, 1)

        # Логические операции
        ops_box = QGroupBox("Логические операции (в любой системе)")
        ops_layout = QGridLayout(); ops_box.setLayout(ops_layout)
        ops_layout.setHorizontalSpacing(10); ops_layout.setVerticalSpacing(8)
        layout.addWidget(ops_box)

        self.op_a = QLineEdit(); self.op_b = QLineEdit()
        self.op_base = QComboBox(); self.op_base.addItems(["BIN", "OCT", "DEC", "HEX"]); self.op_base.setCurrentText("HEX")
        and_btn = AnimatedButton("A AND B"); and_btn.clicked.connect(lambda: self.prog_logic("AND"))
        or_btn = AnimatedButton("A OR B"); or_btn.clicked.connect(lambda: self.prog_logic("OR"))
        xor_btn = AnimatedButton("A XOR B"); xor_btn.clicked.connect(lambda: self.prog_logic("XOR"))
        not_btn = AnimatedButton("NOT A"); not_btn.clicked.connect(lambda: self.prog_logic("NOT"))
        for b in [and_btn, or_btn, xor_btn, not_btn]:
            b.setStyleSheet(self.styles.get_operator_style())

        self.op_result = QLineEdit(); self.op_result.setReadOnly(True)

        ops_layout.addWidget(QLabel("A"), 0, 0); ops_layout.addWidget(self.op_a, 0, 1)
        ops_layout.addWidget(QLabel("B"), 1, 0); ops_layout.addWidget(self.op_b, 1, 1)
        ops_layout.addWidget(QLabel("Base"), 2, 0); ops_layout.addWidget(self.op_base, 2, 1)
        ops_layout.addWidget(and_btn, 0, 2); ops_layout.addWidget(or_btn, 0, 3)
        ops_layout.addWidget(xor_btn, 1, 2); ops_layout.addWidget(not_btn, 1, 3)
        ops_layout.addWidget(QLabel("Результат"), 2, 2); ops_layout.addWidget(self.op_result, 2, 3)

        # Битовый сдвиг
        shift_box = QGroupBox("Битовый сдвиг")
        shift_layout = QGridLayout(); shift_box.setLayout(shift_layout)
        shift_layout.setHorizontalSpacing(10); shift_layout.setVerticalSpacing(8)
        layout.addWidget(shift_box)

        self.shift_input = QLineEdit(); self.shift_bits = QLineEdit(); self.shift_bits.setPlaceholderText("на сколько")
        self.shift_base = QComboBox(); self.shift_base.addItems(["BIN", "DEC", "HEX"])
        left_btn = AnimatedButton("<<"); left_btn.clicked.connect(lambda: self.prog_shift("LEFT"))
        right_btn = AnimatedButton(">>"); right_btn.clicked.connect(lambda: self.prog_shift("RIGHT"))
        for b in [left_btn, right_btn]:
            b.setStyleSheet(self.styles.get_operator_style())

        self.shift_bin = QLineEdit(); self.shift_bin.setReadOnly(True)
        shift_layout.addWidget(QLabel("Число"), 0, 0); shift_layout.addWidget(self.shift_input, 0, 1)
        shift_layout.addWidget(QLabel("Base"), 0, 2); shift_layout.addWidget(self.shift_base, 0, 3)
        shift_layout.addWidget(QLabel("Сдвиг"), 1, 0); shift_layout.addWidget(self.shift_bits, 1, 1)
        shift_layout.addWidget(left_btn, 1, 2); shift_layout.addWidget(right_btn, 1, 3)
        shift_layout.addWidget(QLabel("BIN"), 2, 0); shift_layout.addWidget(self.shift_bin, 2, 1, 1, 3)

        # Цветовые модели
        color_box = QGroupBox("Цветовые модели")
        color_layout = QGridLayout(); color_box.setLayout(color_layout)
        color_layout.setHorizontalSpacing(10); color_layout.setVerticalSpacing(8)
        layout.addWidget(color_box)

        self.color_hex = QLineEdit(); self.color_hex.setPlaceholderText("#RRGGBB")
        color_btn = AnimatedButton("Преобразовать"); color_btn.clicked.connect(self.prog_color_convert)
        color_btn.setStyleSheet(self.styles.get_function_style())
        self.color_rgb = QLineEdit(); self.color_hsl = QLineEdit(); self.color_cmyk = QLineEdit()
        for e in [self.color_rgb, self.color_hsl, self.color_cmyk]:
            e.setReadOnly(True)
        color_layout.addWidget(QLabel("HEX"), 0, 0); color_layout.addWidget(self.color_hex, 0, 1)
        color_layout.addWidget(color_btn, 0, 2)
        color_layout.addWidget(QLabel("RGB"), 1, 0); color_layout.addWidget(self.color_rgb, 1, 1, 1, 2)
        color_layout.addWidget(QLabel("HSL"), 2, 0); color_layout.addWidget(self.color_hsl, 2, 1, 1, 2)
        color_layout.addWidget(QLabel("CMYK"), 3, 0); color_layout.addWidget(self.color_cmyk, 3, 1, 1, 2)

        # UNIX time и генератор
        misc_box = QGroupBox("UNIX-время и генератор паролей")
        misc_layout = QGridLayout(); misc_box.setLayout(misc_layout)
        misc_layout.setHorizontalSpacing(10); misc_layout.setVerticalSpacing(8)
        layout.addWidget(misc_box)

        self.unix_input = QLineEdit(); self.unix_input.setPlaceholderText("UNIX timestamp или дата YYYY-MM-DD HH:MM:SS")
        unix_to_date = AnimatedButton("→ Дата"); unix_to_date.setStyleSheet(self.styles.get_function_style())
        date_to_unix = AnimatedButton("→ UNIX"); date_to_unix.setStyleSheet(self.styles.get_function_style())
        unix_to_date.clicked.connect(lambda: self.prog_unix_convert("to_date"))
        date_to_unix.clicked.connect(lambda: self.prog_unix_convert("to_unix"))
        self.unix_result = QLineEdit(); self.unix_result.setReadOnly(True)
        misc_layout.addWidget(self.unix_input, 0, 0, 1, 2)
        misc_layout.addWidget(unix_to_date, 0, 2); misc_layout.addWidget(date_to_unix, 0, 3)
        misc_layout.addWidget(self.unix_result, 1, 0, 1, 4)

        self.pass_len = QLineEdit(); self.pass_len.setPlaceholderText("Длина")
        self.pass_chars = QLineEdit(); self.pass_chars.setPlaceholderText("Набор символов (пусто = стандарт)")
        self.pass_exclude_similar = QCheckBox("Исключить похожие (O0Il1)")
        gen_btn = AnimatedButton("Сгенерировать пароль")
        gen_btn.setStyleSheet(self.styles.get_more_button_style())
        gen_btn.clicked.connect(self.prog_generate_password)
        self.pass_result = QLineEdit(); self.pass_result.setReadOnly(True)
        misc_layout.addWidget(self.pass_len, 2, 0)
        misc_layout.addWidget(self.pass_chars, 2, 1)
        misc_layout.addWidget(self.pass_exclude_similar, 2, 2)
        misc_layout.addWidget(gen_btn, 2, 3)
        misc_layout.addWidget(self.pass_result, 3, 0, 1, 4)

        layout.addStretch(1)
        return widget

    def create_graph_tab(self):
        """Создает вкладку построения графиков (заготовка UI)"""
        widget = QWidget()
        layout = QVBoxLayout(); widget.setLayout(layout)
        layout.setSpacing(10); layout.setContentsMargins(0, 0, 0, 0)

        top = QHBoxLayout(); layout.addLayout(top)
        self.graph_expr = QLineEdit(); self.graph_expr.setPlaceholderText("f(x) = sin(x)/x")
        plot_btn = AnimatedButton("Построить график")
        plot_btn.setStyleSheet(self.styles.get_function_style())
        plot_btn.clicked.connect(self.plot_graph)
        top.addWidget(QLabel("f(x) =")); top.addWidget(self.graph_expr, 1); top.addWidget(plot_btn)

        # Контейнер + фиксируем layout один раз
        self.graph_canvas_container = QWidget()
        self.graph_canvas_layout = QVBoxLayout(self.graph_canvas_container)
        self.graph_canvas_layout.setContentsMargins(6,6,6,6)
        layout.addWidget(self.graph_canvas_container, 1)

        return widget

    def create_display(self):
        display = QTextEdit()
        display.setFont(QFont('Arial', 28))
        display.setAlignment(Qt.AlignRight)
        display.setReadOnly(False)  # Разрешаем редактирование
        display.setMaximumHeight(90)
        display.setMinimumHeight(90)
        display.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        display.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        display.textChanged.connect(self.on_display_text_changed)
        return display

    def on_display_text_changed(self):
        """Обновляет current_input при изменении текста в дисплее"""
        # Определяем, какой дисплей использовать
        current_tab = self.tab_widget.currentIndex()
        if current_tab == 0:  # Стандартный калькулятор
            self.current_input = self.basic_display.toPlainText()
        elif current_tab == 1:  # Научный калькулятор
            self.current_input = self.scientific_display.toPlainText()

    def format_text_with_rainbow_colors(self, text):
        """Форматирует текст с радужными цветами для цифр и операторов"""
        # Радужные цвета для цифр
        rainbow_colors = {
            '0': '#ff0000',  # Красный
            '1': '#ff8000',  # Оранжевый
            '2': '#ffff00',  # Желтый
            '3': '#80ff00',  # Желто-зеленый
            '4': '#00ff00',  # Зеленый
            '5': '#00ff80',  # Зелено-голубой
            '6': '#00ffff',  # Голубой
            '7': '#0080ff',  # Синий
            '8': '#0000ff',  # Синий
            '9': '#8000ff',  # Фиолетовый
        }
        
        # Радужные цвета для операторов
        operator_colors = {
            '+': '#ff0080',  # Розовый
            '-': '#ff4000',  # Красно-оранжевый
            '*': '#ff8000',  # Оранжевый
            '/': '#ffff00',  # Желтый
            '=': '#00ff00',  # Зеленый
            '×': '#ff8000',  # Оранжевый
            '÷': '#ffff00',  # Желтый
            '^': '#ff00ff',  # Пурпурный
            '√': '#00ff80',  # Зелено-голубой
            'sin': '#ff80ff',  # Светло-пурпурный
            'cos': '#80ffff',  # Светло-голубой
            'tan': '#ffff80',  # Светло-желтый
            'log': '#80ff80',  # Светло-зеленый
            'ln': '#ff8080',  # Светло-красный
            'x²': '#ff4080',  # Розово-красный
            'x³': '#ff8040',  # Оранжево-красный
            'x!': '#40ff80',  # Зелено-голубой
            '1/x': '#8040ff',  # Фиолетово-синий
            '10^x': '#ff8040',  # Оранжево-красный
            'e^x': '#40ff40',  # Зеленый
            '|x|': '#ff4040',  # Красный
            '2^x': '#4040ff',  # Синий
            '∛': '#80ff40',  # Желто-зеленый
            'n!': '#ff40ff',  # Пурпурный
            'rand': '#40ffff',  # Голубой
            '!': '#ff8080',  # Светло-красный
        }
        
        formatted_text = ""
        i = 0
        while i < len(text):
            # Проверяем многосимвольные функции
            found_function = False
            for func in ['x²', 'x³', 'x!', '1/x', '10^x', 'e^x', '|x|', '2^x', '∛', 'n!', 'rand', 'sin', 'cos', 'tan', 'log', 'ln', 'sqrt']:
                if text[i:i+len(func)] == func:
                    color = operator_colors.get(func, '#ffffff')
                    formatted_text += f'<span style="color: {color};">{func}</span>'
                    i += len(func)
                    found_function = True
                    break
            
            if not found_function:
                char = text[i]
                if char in rainbow_colors:
                    color = rainbow_colors[char]
                    formatted_text += f'<span style="color: {color};">{char}</span>'
                elif char in operator_colors:
                    color = operator_colors[char]
                    formatted_text += f'<span style="color: {color};">{char}</span>'
                else:
                    formatted_text += char
                i += 1
        
        return formatted_text

    # ===== Реализация действий вкладки Программист (минимальная логика) =====
    def _to_int(self, value_text, base_name):
        bases = {"BIN":2, "OCT":8, "DEC":10, "HEX":16}
        base = bases[base_name]
        text = value_text.strip()
        if base_name == "HEX" and text.upper().startswith("0X"):
            text = text[2:]
        return int(text, base)

    def _from_int_all(self, value_int):
        return (
            bin(value_int)[2:],
            oct(value_int)[2:],
            str(value_int),
            hex(value_int)[2:].upper(),
        )

    def prog_convert(self):
        try:
            value = self._to_int(self.prog_input.text(), self.prog_base.currentText())
            b, o, d, h = self._from_int_all(value)
            self.out_bin.setText(b)
            self.out_oct.setText(o)
            self.out_dec.setText(d)
            self.out_hex.setText(h)
        except Exception as e:
            self.show_error(f"Некорректное число: {str(e)}")

    def prog_logic(self, op):
        try:
            a = self._to_int(self.op_a.text(), self.op_base.currentText()) if self.op_a.text() else 0
            b = self._to_int(self.op_b.text(), self.op_base.currentText()) if self.op_b.text() else 0
            if op == "AND":
                r = a & b
            elif op == "OR":
                r = a | b
            elif op == "XOR":
                r = a ^ b
            elif op == "NOT":
                r = ~a & ((1 << max(a.bit_length(), 1)) - 1)
            else:
                return
            # выводим в выбранной системе
            bases = {"BIN": bin, "OCT": oct, "DEC": lambda x: str(x), "HEX": lambda x: hex(x).upper()}
            fmt = bases[self.op_base.currentText()]
            out = fmt(r)
            if out.startswith("0B") or out.startswith("0O") or out.startswith("0X"):
                out = out[2:]
            self.op_result.setText(out)
        except Exception as e:
            self.show_error(f"Ошибка логической операции: {str(e)}")

    def prog_shift(self, direction):
        try:
            val = self._to_int(self.shift_input.text(), self.shift_base.currentText())
            bits = int(self.shift_bits.text())
            if direction == "LEFT":
                val = val << bits
            else:
                val = val >> bits
            self.shift_bin.setText(bin(val)[2:])
        except Exception as e:
            self.show_error(f"Ошибка сдвига: {str(e)}")

    def prog_color_convert(self):
        try:
            text = self.color_hex.text().strip()
            if text.startswith('#'):
                text = text[1:]
            if len(text) != 6:
                raise ValueError("HEX должен быть вида #RRGGBB")
            r = int(text[0:2], 16); g = int(text[2:4], 16); b = int(text[4:6], 16)
            self.color_rgb.setText(f"{r}, {g}, {b}")
            # HSL
            import colorsys
            h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
            self.color_hsl.setText(f"{int(h*360)}°, {int(s*100)}%, {int(l*100)}%")
            # CMYK
            if (r, g, b) == (0, 0, 0):
                c = m = y = 0; k = 100
            else:
                c = 1 - r/255; m = 1 - g/255; y = 1 - b/255
                k = min(c, m, y)
                c = int((c - k) / (1 - k) * 100)
                m = int((m - k) / (1 - k) * 100)
                y = int((y - k) / (1 - k) * 100)
                k = int(k * 100)
            self.color_cmyk.setText(f"C{c} M{m} Y{y} K{k}")
        except Exception as e:
            self.show_error(f"Ошибка преобразования цвета: {str(e)}")

    def prog_unix_convert(self, mode):
        try:
            from datetime import datetime
            if mode == "to_date":
                ts = int(float(self.unix_input.text()))
                dt = datetime.fromtimestamp(ts)
                self.unix_result.setText(dt.strftime("%Y-%m-%d %H:%M:%S"))
            else:
                dt = datetime.strptime(self.unix_input.text().strip(), "%Y-%m-%d %H:%M:%S")
                self.unix_result.setText(str(int(dt.timestamp())))
        except Exception as e:
            self.show_error(f"Ошибка преобразования времени: {str(e)}")

    def prog_generate_password(self):
        import random, string
        try:
            length = int(self.pass_len.text()) if self.pass_len.text() else 12
            chars = self.pass_chars.text() or (string.ascii_letters + string.digits + "!@#$%^&*()")
            if self.pass_exclude_similar.isChecked():
                for ch in "O0Il1":
                    chars = chars.replace(ch, "")
            if not chars:
                raise ValueError("Набор символов пуст")
            self.pass_result.setText(''.join(random.choice(chars) for _ in range(length)))
        except Exception as e:
            self.show_error(f"Ошибка генерации: {str(e)}")

    # ===== Построение графиков (заготовка) =====
    def plot_graph(self):
        try:
            import math
            import numpy as np
            from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
            from matplotlib.figure import Figure

            expr = self.graph_expr.text().strip() or "sin(x)/x"

            # Создаем фигуру
            fig = Figure(figsize=(5, 3), tight_layout=True)
            canvas = FigureCanvas(fig)
            ax = fig.add_subplot(111)

            xs = np.linspace(-10, 10, 1000)
            safe = {
                'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
                'log': np.log10, 'ln': np.log, 'sqrt': np.sqrt,
                'pi': math.pi, 'e': math.e, 'abs': np.abs,
                'exp': np.exp, '__builtins__': {}
            }
            # Поддержка синтаксиса f(x) = ...
            s = expr
            if '=' in s:
                s = s.split('=', 1)[1]
            s = s.replace('^', '**')
            ys = eval(s, safe, {'x': xs})

            ax.plot(xs, ys, color='#67b7ff')
            ax.axhline(0, color='#888888', linewidth=0.8)
            ax.axvline(0, color='#888888', linewidth=0.8)
            ax.grid(True, alpha=0.3)
            ax.set_title(f"f(x) = {expr}")

            # Заменяем содержимое контейнера (пересоздавать layout не будем)
            while self.graph_canvas_layout.count():
                item = self.graph_canvas_layout.takeAt(0)
                if item.widget():
                    item.widget().setParent(None)
            self.graph_canvas_layout.addWidget(canvas)
        except Exception as e:
            self.show_error(f"Ошибка построения графика: {str(e)}")

    def create_basic_calculator(self):
        """Создает стандартный калькулятор"""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)

        # Создаем дисплей для этого калькулятора
        self.basic_display = self.create_display()
        layout.addWidget(self.basic_display)

        # Создаем кнопки
        button_layout = QGridLayout()
        layout.addLayout(button_layout)
        button_layout.setSpacing(8)

        # Кнопки для стандартного калькулятора
        basic_buttons = [
            ('AC', 0, 0), ('%', 0, 1), ('⌫', 0, 2), ('÷', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('×', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('±', 4, 0), ('0', 4, 1), ('.', 4, 2), ('=', 4, 3),
            ('Помощь', 5, 0, 1, 4),  # Кнопка помощи на всю ширину
        ]

        for button_data in basic_buttons:
            if len(button_data) == 5:  # Кнопка с расширенным размером
                text, row, col, rowspan, colspan = button_data
                btn = self.create_calculator_button(text)
                button_layout.addWidget(btn, row, col, rowspan, colspan)
            else:  # Обычная кнопка
                text, row, col = button_data
                btn = self.create_calculator_button(text)
                button_layout.addWidget(btn, row, col)

        return widget

    def create_scientific_calculator(self):
        """Создает научный калькулятор с компактным расположением"""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)

        # Создаем дисплей для научного калькулятора
        self.scientific_display = self.create_display()
        layout.addWidget(self.scientific_display)

        # Создаем кнопки в компактном расположении
        button_layout = QGridLayout()
        layout.addLayout(button_layout)
        button_layout.setSpacing(6)

        # Каноничное расположение кнопок для научного калькулятора на одном уровне
        scientific_buttons = [
            # Первый ряд - функции очистки, константы и операторы
            ('AC', 0, 0), ('C', 0, 1), ('⌫', 0, 2), ('π', 0, 3), ('e', 0, 4), ('÷', 0, 5), ('×', 0, 6), ('-', 0, 7), ('+', 0, 8),
            # Второй ряд - тригонометрические функции и цифры 7,8,9
            ('sin', 1, 0), ('cos', 1, 1), ('tan', 1, 2), ('log', 1, 3), ('ln', 1, 4), ('7', 1, 5), ('8', 1, 6), ('9', 1, 7), ('%', 1, 8),
            # Третий ряд - степени, корни, скобки и цифры 4,5,6
            ('x²', 2, 0), ('x^y', 2, 1), ('√', 2, 2), ('(', 2, 3), (')', 2, 4), ('4', 2, 5), ('5', 2, 6), ('6', 2, 7), ('=', 2, 8, 1, 2),
            # Четвертый ряд - дополнительные функции и цифры 1,2,3
            ('x!', 3, 0), ('1/x', 3, 1), ('10^x', 3, 2), ('e^x', 3, 3), ('|x|', 3, 4), ('1', 3, 5), ('2', 3, 6), ('3', 3, 7), ('', 3, 8),
            # Пятый ряд - дополнительные функции и цифры 0, точка, знак
            ('2^x', 4, 0), ('x³', 4, 1), ('∛', 4, 2), ('n!', 4, 3), ('rand', 4, 4), ('±', 4, 5), ('0', 4, 6), ('.', 4, 7), ('', 4, 8),
            # Шестой ряд - кнопка помощи
            ('Помощь', 5, 0, 1, 9),  # Кнопка помощи на всю ширину
        ]

        for button_data in scientific_buttons:
            if len(button_data) == 5:  # Кнопка с расширенным размером
                text, row, col, rowspan, colspan = button_data
                btn = self.create_calculator_button(text)
                button_layout.addWidget(btn, row, col, rowspan, colspan)
            else:  # Обычная кнопка
                text, row, col = button_data
                if text:  # Пропускаем пустые кнопки
                    btn = self.create_calculator_button(text)
                    button_layout.addWidget(btn, row, col)

        return widget

    def create_notes_window(self):
        """Создает окно заметок: список + редактор. Создание сразу открывает редактирование."""
        widget = QWidget()
        layout = QHBoxLayout(); widget.setLayout(layout)
        layout.setContentsMargins(6,6,6,6)

        # Левая колонка: список заметок
        left = QVBoxLayout(); layout.addLayout(left, 1)
        header = QLabel("📝 Заметки"); header.setFont(QFont('Arial', 14, QFont.Bold)); header.setAlignment(Qt.AlignCenter)
        left.addWidget(header)

        self.notes_list_widget = QListWidget()
        self.notes_list_widget.itemClicked.connect(self.on_note_selected)
        left.addWidget(self.notes_list_widget, 1)

        left_buttons = QHBoxLayout(); left.addLayout(left_buttons)
        add_btn = AnimatedButton("➕ Создать"); add_btn.setStyleSheet(self.styles.get_help_button_style())
        add_btn.clicked.connect(self.create_new_note)
        del_btn = AnimatedButton("🗑️ Удалить"); del_btn.setStyleSheet(self.styles.get_back_button_style())
        del_btn.clicked.connect(self.delete_selected_note)
        left_buttons.addWidget(add_btn); left_buttons.addWidget(del_btn)

        # Правая колонка: редактор
        right = QVBoxLayout(); layout.addLayout(right, 2)
        self.note_title = QLineEdit(); self.note_title.setPlaceholderText("Название заметки")
        self.note_editor = QTextEdit(); self.note_editor.setPlaceholderText("Текст заметки...")
        save_btn = AnimatedButton("💾 Сохранить"); save_btn.setStyleSheet(self.styles.get_financial_button_style())
        save_btn.clicked.connect(self.save_current_note)
        right.addWidget(self.note_title); right.addWidget(self.note_editor, 1); right.addWidget(save_btn)

        # Данные
        self.notes = []  # список словарей {id,title,content}
        self.note_counter = 1
        self.current_note_id = None

        return widget

    def create_financial_calculator(self):
        """Создает финансовый калькулятор"""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)

        # Заголовок
        title_label = QLabel("💰 Финансовый калькулятор")
        title_label.setFont(QFont('Arial', 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Вкладки для финансового калькулятора
        self.financial_tabs = QTabWidget()
        layout.addWidget(self.financial_tabs)

        # Вкладка валют
        currency_tab = self.create_currency_tab()
        self.financial_tabs.addTab(currency_tab, "💱 Валюты")

        # Вкладка кредитов
        credit_tab = self.create_credit_tab()
        self.financial_tabs.addTab(credit_tab, "🏦 Кредиты")

        # Вкладка ипотеки
        mortgage_tab = self.create_mortgage_tab()
        self.financial_tabs.addTab(mortgage_tab, "🏠 Ипотека")

        # Вкладка накоплений
        savings_tab = self.create_savings_tab()
        self.financial_tabs.addTab(savings_tab, "💎 Накопления")

        return widget

    def create_currency_tab(self):
        """Создает вкладку конвертера валют"""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # Заголовок
        title = QLabel("💱 Конвертер валют")
        title.setFont(QFont('Arial', 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Информация о курсах
        self.currency_info = QLabel("Курсы валют загружаются...")
        self.currency_info.setFont(QFont('Arial', 10))
        self.currency_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.currency_info)

        # Поля ввода
        input_layout = QGridLayout()
        
        # Сумма
        input_layout.addWidget(QLabel("Сумма:"), 0, 0)
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Введите сумму")
        input_layout.addWidget(self.amount_input, 0, 1)

        # Из валюты
        input_layout.addWidget(QLabel("Из валюты:"), 1, 0)
        self.from_currency = QComboBox()
        self.from_currency.setEditable(True)
        # Валюты, доступные в API Беларусбанка
        self.from_currency.addItems(["BYN", "USD", "EUR", "RUB", "UAH", "PLN", "GBP", "CHF", "JPY", "CNY", "CAD", "AUD", "SEK", "NOK", "DKK", "CZK", "HUF", "BGN", "RON", "HRK", "RSD", "BAM", "MKD", "ALL", "ISK", "MDL", "UZS", "KZT", "KGS", "TJS", "AMD", "AZN", "GEL", "TRY", "ILS", "AED", "SAR", "QAR", "KWD", "BHD", "OMR", "JOD", "LBP", "EGP", "MAD", "TND", "DZD", "ZAR", "NGN", "KES", "UGX", "TZS", "ETB", "GHS", "XOF", "XAF", "CDF", "AOA", "MZN", "BWP", "SZL", "LSL", "NAD", "ZMW", "MWK", "BIF", "RWF", "DJF", "SOS", "KMF", "MUR", "SCR", "MVR", "LKR", "BDT", "NPR", "PKR", "AFN", "IRR", "IQD", "SYP", "YER", "INR", "IDR", "MYR", "SGD", "THB", "VND", "PHP", "KRW", "TWD", "HKD", "MOP", "BND", "LAK", "KHR", "MMK", "MNT", "NPR", "BTN", "LKR", "MVR", "SCR", "MUR", "KMF", "SOS", "DJF", "RWF", "BIF", "MWK", "ZMW", "NAD", "LSL", "SZL", "BWP", "MZN", "AOA", "CDF", "XAF", "XOF", "GHS", "ETB", "TZS", "UGX", "KES", "NGN", "ZAR", "DZD", "TND", "MAD", "EGP", "LBP", "JOD", "OMR", "BHD", "KWD", "QAR", "SAR", "AED", "ILS", "TRY", "GEL", "AZN", "AMD", "TJS", "KGS", "KZT", "UZS", "MDL", "ISK", "ALL", "MKD", "BAM", "RSD", "HRK", "RON", "BGN", "HUF", "CZK", "DKK", "NOK", "SEK", "AUD", "CAD", "CNY", "JPY", "CHF", "GBP", "PLN", "UAH", "RUB", "EUR", "USD"])
        self.from_currency.setCurrentText("USD")
        input_layout.addWidget(self.from_currency, 1, 1)

        # В валюту
        input_layout.addWidget(QLabel("В валюту:"), 2, 0)
        self.to_currency = QComboBox()
        self.to_currency.setEditable(True)
        # Валюты, доступные в API Беларусбанка
        self.to_currency.addItems(["BYN", "USD", "EUR", "RUB", "UAH", "PLN", "GBP", "CHF", "JPY", "CNY", "CAD", "AUD", "SEK", "NOK", "DKK", "CZK", "HUF", "BGN", "RON", "HRK", "RSD", "BAM", "MKD", "ALL", "ISK", "MDL", "UZS", "KZT", "KGS", "TJS", "AMD", "AZN", "GEL", "TRY", "ILS", "AED", "SAR", "QAR", "KWD", "BHD", "OMR", "JOD", "LBP", "EGP", "MAD", "TND", "DZD", "ZAR", "NGN", "KES", "UGX", "TZS", "ETB", "GHS", "XOF", "XAF", "CDF", "AOA", "MZN", "BWP", "SZL", "LSL", "NAD", "ZMW", "MWK", "BIF", "RWF", "DJF", "SOS", "KMF", "MUR", "SCR", "MVR", "LKR", "BDT", "NPR", "PKR", "AFN", "IRR", "IQD", "SYP", "YER", "INR", "IDR", "MYR", "SGD", "THB", "VND", "PHP", "KRW", "TWD", "HKD", "MOP", "BND", "LAK", "KHR", "MMK", "MNT", "NPR", "BTN", "LKR", "MVR", "SCR", "MUR", "KMF", "SOS", "DJF", "RWF", "BIF", "MWK", "ZMW", "NAD", "LSL", "SZL", "BWP", "MZN", "AOA", "CDF", "XAF", "XOF", "GHS", "ETB", "TZS", "UGX", "KES", "NGN", "ZAR", "DZD", "TND", "MAD", "EGP", "LBP", "JOD", "OMR", "BHD", "KWD", "QAR", "SAR", "AED", "ILS", "TRY", "GEL", "AZN", "AMD", "TJS", "KGS", "KZT", "UZS", "MDL", "ISK", "ALL", "MKD", "BAM", "RSD", "HRK", "RON", "BGN", "HUF", "CZK", "DKK", "NOK", "SEK", "AUD", "CAD", "CNY", "JPY", "CHF", "GBP", "PLN", "UAH", "RUB", "EUR", "USD"])
        self.to_currency.setCurrentText("EUR")
        input_layout.addWidget(self.to_currency, 2, 1)

        layout.addLayout(input_layout)

        # Кнопки конвертации
        button_layout = QHBoxLayout()
        convert_btn = AnimatedButton("🔄 Конвертировать")
        convert_btn.clicked.connect(self.convert_currency)
        convert_btn.setStyleSheet(self.styles.get_currency_button_style())
        refresh_btn = AnimatedButton("🔄 Обновить курсы")
        refresh_btn.clicked.connect(self.refresh_currency_rates)
        refresh_btn.setStyleSheet(self.styles.get_financial_button_style())
        button_layout.addWidget(convert_btn)
        button_layout.addWidget(refresh_btn)
        layout.addLayout(button_layout)

        # Результат
        self.currency_result = QLabel("")
        self.currency_result.setFont(QFont('Arial', 12, QFont.Bold))
        self.currency_result.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.currency_result)

        return widget

    def create_credit_tab(self):
        """Создает вкладку расчета кредитов"""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        title = QLabel("🏦 Расчет кредита")
        title.setFont(QFont('Arial', 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Поля ввода
        input_layout = QGridLayout()
        
        input_layout.addWidget(QLabel("Сумма кредита:"), 0, 0)
        self.credit_amount = QLineEdit()
        self.credit_amount.setPlaceholderText("100000")
        input_layout.addWidget(self.credit_amount, 0, 1)

        input_layout.addWidget(QLabel("Валюта:"), 1, 0)
        self.credit_currency = QComboBox()
        self.credit_currency.addItems(["BYN", "USD", "EUR", "CNY"])
        self.credit_currency.setCurrentText("BYN")
        input_layout.addWidget(self.credit_currency, 1, 1)

        input_layout.addWidget(QLabel("Процентная ставка (%):"), 2, 0)
        self.credit_rate = QLineEdit()
        self.credit_rate.setPlaceholderText("12")
        input_layout.addWidget(self.credit_rate, 2, 1)

        input_layout.addWidget(QLabel("Срок (месяцев):"), 3, 0)
        self.credit_term = QLineEdit()
        self.credit_term.setPlaceholderText("36")
        input_layout.addWidget(self.credit_term, 3, 1)

        layout.addLayout(input_layout)

        # Кнопка расчета
        calculate_btn = AnimatedButton("📊 Рассчитать")
        calculate_btn.clicked.connect(self.calculate_credit)
        calculate_btn.setStyleSheet(self.styles.get_financial_button_style())
        layout.addWidget(calculate_btn)

        # Результат
        self.credit_result = QLabel("")
        self.credit_result.setFont(QFont('Arial', 10))
        layout.addWidget(self.credit_result)

        return widget

    def create_mortgage_tab(self):
        """Создает вкладку расчета ипотеки"""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        title = QLabel("🏠 Расчет ипотеки")
        title.setFont(QFont('Arial', 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Поля ввода
        input_layout = QGridLayout()
        
        input_layout.addWidget(QLabel("Стоимость недвижимости:"), 0, 0)
        self.mortgage_amount = QLineEdit()
        self.mortgage_amount.setPlaceholderText("5000000")
        input_layout.addWidget(self.mortgage_amount, 0, 1)

        input_layout.addWidget(QLabel("Валюта:"), 1, 0)
        self.mortgage_currency = QComboBox()
        self.mortgage_currency.addItems(["BYN", "USD", "EUR", "CNY"])
        self.mortgage_currency.setCurrentText("BYN")
        input_layout.addWidget(self.mortgage_currency, 1, 1)

        input_layout.addWidget(QLabel("Первоначальный взнос:"), 2, 0)
        self.mortgage_down = QLineEdit()
        self.mortgage_down.setPlaceholderText("1000000")
        input_layout.addWidget(self.mortgage_down, 2, 1)

        input_layout.addWidget(QLabel("Процентная ставка (%):"), 3, 0)
        self.mortgage_rate = QLineEdit()
        self.mortgage_rate.setPlaceholderText("8")
        input_layout.addWidget(self.mortgage_rate, 3, 1)

        input_layout.addWidget(QLabel("Срок (лет):"), 4, 0)
        self.mortgage_term = QLineEdit()
        self.mortgage_term.setPlaceholderText("20")
        input_layout.addWidget(self.mortgage_term, 4, 1)

        layout.addLayout(input_layout)

        # Кнопка расчета
        calculate_btn = AnimatedButton("📊 Рассчитать")
        calculate_btn.clicked.connect(self.calculate_mortgage)
        calculate_btn.setStyleSheet(self.styles.get_financial_button_style())
        layout.addWidget(calculate_btn)

        # Результат
        self.mortgage_result = QLabel("")
        self.mortgage_result.setFont(QFont('Arial', 10))
        layout.addWidget(self.mortgage_result)

        return widget

    def create_savings_tab(self):
        """Создает вкладку расчета накоплений"""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        title = QLabel("💎 Расчет накоплений")
        title.setFont(QFont('Arial', 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Поля ввода
        input_layout = QGridLayout()
        
        input_layout.addWidget(QLabel("Ежемесячный взнос:"), 0, 0)
        self.savings_monthly = QLineEdit()
        self.savings_monthly.setPlaceholderText("10000")
        input_layout.addWidget(self.savings_monthly, 0, 1)

        input_layout.addWidget(QLabel("Валюта:"), 1, 0)
        self.savings_currency = QComboBox()
        self.savings_currency.addItems(["BYN", "USD", "EUR", "CNY"])
        self.savings_currency.setCurrentText("BYN")
        input_layout.addWidget(self.savings_currency, 1, 1)

        input_layout.addWidget(QLabel("Процентная ставка (%):"), 2, 0)
        self.savings_rate = QLineEdit()
        self.savings_rate.setPlaceholderText("6")
        input_layout.addWidget(self.savings_rate, 2, 1)

        input_layout.addWidget(QLabel("Срок (лет):"), 3, 0)
        self.savings_term = QLineEdit()
        self.savings_term.setPlaceholderText("10")
        input_layout.addWidget(self.savings_term, 3, 1)

        layout.addLayout(input_layout)

        # Кнопка расчета
        calculate_btn = AnimatedButton("📊 Рассчитать")
        calculate_btn.clicked.connect(self.calculate_savings)
        calculate_btn.setStyleSheet(self.styles.get_financial_button_style())
        layout.addWidget(calculate_btn)

        # Результат
        self.savings_result = QLabel("")
        self.savings_result.setFont(QFont('Arial', 10))
        layout.addWidget(self.savings_result)

        return widget

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
            ('Помощь', 5, 0, 1, 4),  # Кнопка помощи на всю ширину
        ]

        for button_data in basic_buttons:
            if len(button_data) == 5:  # Кнопка с расширенным размером
                text, row, col, rowspan, colspan = button_data
                btn = self.create_calculator_button(text)
                layout.addWidget(btn, row, col, rowspan, colspan)
            else:  # Обычная кнопка
                text, row, col = button_data
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
                layout.addWidget(btn, row, col)

        return widget

    def create_calculator_button(self, text):
        """Создает кнопку калькулятора с анимацией и звуком"""
        btn = AnimatedButton(text)
        btn.setFont(QFont('Arial', 16))
        btn.setMinimumSize(60, 60)
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Подключаем обработчик клика
        if text not in ['≡', 'Назад', 'Помощь']:
            btn.clicked.connect(lambda: self.on_button_click(text))
        elif text == '≡':
            btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        elif text == 'Назад':
            btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        elif text == 'Помощь':
            btn.clicked.connect(self.show_step_by_step_help)

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
        elif text == 'Помощь':
            btn.setStyleSheet(self.styles.get_help_button_style())
        else:
            btn.setStyleSheet(self.styles.get_number_style())

    def apply_styles(self):
        """Применяет стили к интерфейсу"""
        self.setStyleSheet(self.styles.get_main_style())
        # Применяем стили к дисплеям
        self.basic_display.setStyleSheet(self.styles.get_display_style())
        self.scientific_display.setStyleSheet(self.styles.get_display_style())

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
                    formatted_text = self.format_text_with_rainbow_colors(self.current_input)
                    current_tab = self.tab_widget.currentIndex()
                    if current_tab == 0:
                        self.basic_display.setHtml(formatted_text)
                    elif current_tab == 1:
                        self.scientific_display.setHtml(formatted_text)
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
                formatted_result = self.format_text_with_rainbow_colors(str(result))
                # Определяем, какой дисплей использовать
                current_tab = self.tab_widget.currentIndex()
                if current_tab == 0:  # Стандартный калькулятор
                    self.basic_display.setHtml(formatted_result)
                elif current_tab == 1:  # Научный калькулятор
                    self.scientific_display.setHtml(formatted_result)
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
                        formatted_text = self.format_text_with_rainbow_colors(self.current_input)
                        current_tab = self.tab_widget.currentIndex()
                        if current_tab == 0:
                            self.basic_display.setHtml(formatted_text)
                        elif current_tab == 1:
                            self.scientific_display.setHtml(formatted_text)
                else:
                    # Иначе вычисляем процент от текущего числа
                    value = float(self.current_input) * 0.01
                    self.current_input = str(value)
                    formatted_text = self.format_text_with_rainbow_colors(self.current_input)
                    current_tab = self.tab_widget.currentIndex()
                    if current_tab == 0:
                        self.basic_display.setHtml(formatted_text)
                    elif current_tab == 1:
                        self.scientific_display.setHtml(formatted_text)
                self.result_displayed = False
            except:
                self.show_error("Ошибка вычисления процента")

    def clear_display(self):
        """Очищает дисплей"""
        self.current_input = ""
        # Определяем, какой дисплей использовать
        current_tab = self.tab_widget.currentIndex()
        if current_tab == 0:  # Стандартный калькулятор
            self.basic_display.clear()
        elif current_tab == 1:  # Научный калькулятор
            self.scientific_display.clear()
        self.result_displayed = False
        self.last_result = None

    def backspace(self):
        """Удаляет последний символ"""
        self.current_input = self.current_input[:-1]
        formatted_text = self.format_text_with_rainbow_colors(self.current_input)
        # Определяем, какой дисплей использовать
        current_tab = self.tab_widget.currentIndex()
        if current_tab == 0:  # Стандартный калькулятор
            self.basic_display.setHtml(formatted_text)
        elif current_tab == 1:  # Научный калькулятор
            self.scientific_display.setHtml(formatted_text)
        self.result_displayed = False

    def toggle_sign(self):
        """Меняет знак числа"""
        if self.current_input:
            try:
                if self.current_input[0] == '-':
                    self.current_input = self.current_input[1:]
                else:
                    self.current_input = '-' + self.current_input
                formatted_text = self.format_text_with_rainbow_colors(self.current_input)
                # Определяем, какой дисплей использовать
                current_tab = self.tab_widget.currentIndex()
                if current_tab == 0:  # Стандартный калькулятор
                    self.basic_display.setHtml(formatted_text)
                elif current_tab == 1:  # Научный калькулятор
                    self.scientific_display.setHtml(formatted_text)
            except:
                pass
        self.result_displayed = False

    def add_character(self, char):
        """Добавляет символ в текущий ввод"""
        # Если результат отображен и мы начинаем новое число, очищаем дисплей
        if self.result_displayed and char not in ['+', '-', '*', '/', '×', '÷']:
            self.current_input = ""
            self.result_displayed = False

        # Обрабатываем математические функции - добавляем скобки
        if char in ['sin', 'cos', 'tan', 'log', 'ln', 'sqrt']:
            self.current_input += char + '('
        elif char == 'x²':
            # Для x² добавляем **2 к последнему числу
            if self.current_input and self.current_input[-1].isdigit():
                self.current_input += '**2'
            else:
                self.current_input += '**2'
        elif char == 'x^y':
            # Для x^y добавляем **
            self.current_input += '**'
        elif char == '√':
            # Для квадратного корня добавляем sqrt(
            self.current_input += 'sqrt('
        elif char == 'x!':
            # Факториал
            if self.current_input and self.current_input[-1].isdigit():
                self.current_input += '!'
            else:
                self.current_input += '!'
        elif char == '1/x':
            # Обратное число
            self.current_input += '1/('
        elif char == '10^x':
            # 10 в степени x
            self.current_input += '10**('
        elif char == 'e^x':
            # e в степени x
            self.current_input += 'exp('
        elif char == '|x|':
            # Модуль числа
            self.current_input += 'abs('
        elif char == '2^x':
            # 2 в степени x
            self.current_input += '2**('
        elif char == 'x³':
            # x в кубе
            if self.current_input and self.current_input[-1].isdigit():
                self.current_input += '**3'
            else:
                self.current_input += '**3'
        elif char == '∛':
            # Кубический корень
            self.current_input += 'cbrt('
        elif char == 'n!':
            # Факториал n
            self.current_input += 'factorial('
        elif char == 'rand':
            # Случайное число от 0 до 1
            import random
            self.current_input += str(random.random())
        else:
            self.current_input += char
            
        # Форматируем текст с радужными цветами и отображаем
        formatted_text = self.format_text_with_rainbow_colors(self.current_input)
        # Определяем, какой дисплей использовать в зависимости от активной вкладки
        current_tab = self.tab_widget.currentIndex()
        if current_tab == 0:  # Стандартный калькулятор
            self.basic_display.setHtml(formatted_text)
        elif current_tab == 1:  # Научный калькулятор
            self.scientific_display.setHtml(formatted_text)
        self.result_displayed = False

    def show_error(self, message):
        """Показывает сообщение об ошибке"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Ошибка")
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setStyleSheet(self.styles.get_main_style())
        msg_box.exec_()
        self.clear_display()

    def show_step_by_step_help(self):
        """Показывает пошаговое объяснение текущего выражения"""
        if not self.current_input.strip():
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Помощь")
            msg_box.setText("Введите выражение для получения пошагового объяснения!")
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setStyleSheet(self.styles.get_main_style())
            msg_box.exec_()
            return
        
        try:
            result, steps = self.step_solver.solve_step_by_step(self.current_input)
            
            # Создаем окно с объяснением
            help_window = QMessageBox(self)
            help_window.setWindowTitle("Пошаговое объяснение")
            help_window.setIcon(QMessageBox.Information)
            help_window.setStyleSheet(self.styles.get_main_style())
            
            # Формируем текст объяснения
            explanation_text = "Пошаговое решение:\n\n"
            for step in steps:
                explanation_text += step + "\n"
            
            help_window.setText(explanation_text)
            help_window.setStandardButtons(QMessageBox.Ok)
            help_window.exec_()
            
        except Exception as e:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Ошибка")
            msg_box.setText(f"Не удалось создать пошаговое объяснение: {str(e)}")
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setStyleSheet(self.styles.get_main_style())
            msg_box.exec_()

    # Методы для работы с заметками
    def create_new_note(self):
        """Создает новую заметку и открывает редактор для ввода"""
        note_id = self.note_counter
        self.note_counter += 1
        note = {'id': note_id, 'title': f'Заметка {note_id}', 'content': ''}
        self.notes.append(note)
        item = QListWidgetItem(note['title'])
        item.setData(Qt.UserRole, note_id)
        self.notes_list_widget.addItem(item)
        self.notes_list_widget.setCurrentItem(item)
        self.current_note_id = note_id
        self.note_title.setText(note['title'])
        self.note_editor.setPlainText(note['content'])

    def delete_selected_note(self):
        if not self.notes_list_widget.currentItem():
            return
        note_id = self.notes_list_widget.currentItem().data(Qt.UserRole)
        self.notes = [n for n in self.notes if n['id'] != note_id]
        row = self.notes_list_widget.currentRow()
        self.notes_list_widget.takeItem(row)
        self.current_note_id = None
        self.note_title.clear(); self.note_editor.clear()

    def on_note_selected(self, item):
        note_id = item.data(Qt.UserRole)
        self.current_note_id = note_id
        note = next((n for n in self.notes if n['id'] == note_id), None)
        if note:
            self.note_title.setText(note['title'])
            self.note_editor.setPlainText(note['content'])

    def save_current_note(self):
        if self.current_note_id is None:
            return
        note = next((n for n in self.notes if n['id'] == self.current_note_id), None)
        if not note:
            return
        note['title'] = self.note_title.text() or note['title']
        note['content'] = self.note_editor.toPlainText()
        # Обновляем заголовок в списке
        for i in range(self.notes_list_widget.count()):
            it = self.notes_list_widget.item(i)
            if it.data(Qt.UserRole) == note['id']:
                it.setText(note['title'])
                break

    def delete_note(self):
        """Удаляет заметку"""
        if not self.notes:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Информация")
            msg_box.setText("Нет заметок для удаления!")
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setStyleSheet(self.styles.get_main_style())
            msg_box.exec_()
            return
        
        # Простое удаление последней заметки
        self.notes.pop()
        self.update_notes_display()

    def search_notes(self, search_text):
        """Поиск заметок по названию"""
        if not search_text:
            self.update_notes_display()
            return
        
        filtered_notes = [note for note in self.notes if search_text.lower() in note['title'].lower()]
        
        display_text = ""
        for note in filtered_notes:
            display_text += note['content']
        
        self.notes_list.setText(display_text)

    def update_notes_display(self):
        """Обновляет отображение заметок"""
        display_text = ""
        for note in self.notes:
            display_text += note['content']
        
        self.notes_list.setText(display_text)

    # Методы для финансовых расчетов
    def fetch_currency_rates(self):
        """Получает курсы валют с API Беларусбанка"""
        if not REQUESTS_AVAILABLE:
            return False
            
        try:
            # Проверяем, нужно ли обновлять курсы (обновляем раз в час)
            if (self.last_currency_update and 
                datetime.now() - self.last_currency_update < timedelta(hours=1) and 
                self.currency_rates):
                return True
            
            response = requests.get('https://belarusbank.by/api/kursExchange', timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Очищаем старые курсы
            self.currency_rates = {}
            
            # Обрабатываем данные API
            for bank_data in data:
                if 'kurs' in bank_data:
                    for currency in bank_data['kurs']:
                        curr_code = currency.get('cur_code')
                        if curr_code:
                            # Сохраняем курсы покупки и продажи
                            self.currency_rates[curr_code] = {
                                'buy': float(currency.get('cur_scale', 1)) / float(currency.get('cur_rate', 1)),
                                'sell': float(currency.get('cur_scale', 1)) / float(currency.get('cur_rate', 1)),
                                'scale': int(currency.get('cur_scale', 1))
                            }
            
            self.last_currency_update = datetime.now()
            return True
            
        except Exception as e:
            print(f"Ошибка получения курсов валют: {e}")
            return False
    
    def get_currency_rate(self, from_curr, to_curr):
        """Получает курс конвертации между валютами"""
        if from_curr == to_curr:
            return 1.0
        
        # Если requests недоступна, используем встроенные курсы
        if not REQUESTS_AVAILABLE:
            if from_curr in FALLBACK_RATES and to_curr in FALLBACK_RATES[from_curr]:
                return FALLBACK_RATES[from_curr][to_curr]
            elif to_curr in FALLBACK_RATES and from_curr in FALLBACK_RATES[to_curr]:
                return 1.0 / FALLBACK_RATES[to_curr][from_curr]
            else:
                return None
        
        # Обновляем курсы если нужно
        if not self.fetch_currency_rates():
            # Если не удалось получить курсы с API, используем fallback
            if from_curr in FALLBACK_RATES and to_curr in FALLBACK_RATES[from_curr]:
                return FALLBACK_RATES[from_curr][to_curr]
            elif to_curr in FALLBACK_RATES and from_curr in FALLBACK_RATES[to_curr]:
                return 1.0 / FALLBACK_RATES[to_curr][from_curr]
            return None
        
        # Если одна из валют BYN, используем прямые курсы
        if from_curr == 'BYN' and to_curr in self.currency_rates:
            return self.currency_rates[to_curr]['buy']
        elif to_curr == 'BYN' and from_curr in self.currency_rates:
            return 1.0 / self.currency_rates[from_curr]['sell']
        
        # Для конвертации между двумя не-BYN валютами через BYN
        if from_curr in self.currency_rates and to_curr in self.currency_rates:
            # Конвертируем from_curr -> BYN -> to_curr
            from_to_byn = 1.0 / self.currency_rates[from_curr]['sell']
            byn_to_to = self.currency_rates[to_curr]['buy']
            return from_to_byn * byn_to_to
        
        return None

    def refresh_currency_rates(self):
        """Принудительно обновляет курсы валют"""
        if not REQUESTS_AVAILABLE:
            self.currency_info.setText("Используются встроенные курсы валют\n(для актуальных курсов установите requests)")
            return
            
        self.currency_info.setText("Обновление курсов валют...")
        if self.fetch_currency_rates():
            self.currency_info.setText("Курсы валют успешно обновлены!")
        else:
            self.currency_info.setText("Ошибка обновления курсов валют")

    def convert_currency(self):
        """Конвертирует валюту используя реальные курсы Беларусбанка"""
        amount = self.amount_input.text()
        from_curr = self.from_currency.currentText().upper()
        to_curr = self.to_currency.currentText().upper()
        
        if not amount or not from_curr or not to_curr:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Ошибка")
            msg_box.setText("Заполните все поля!")
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setStyleSheet(self.styles.get_main_style())
            msg_box.exec_()
            return
        
        try:
            amount_float = float(amount)
            
            # Получаем реальный курс
            rate = self.get_currency_rate(from_curr, to_curr)
            
            if rate is None:
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("Ошибка")
                msg_box.setText(f"Не удалось получить курс для конвертации {from_curr} -> {to_curr}.\n"
                    "Проверьте подключение к интернету или попробуйте позже.")
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setStyleSheet(self.styles.get_main_style())
                msg_box.exec_()
                return
            
            result = amount_float * rate
            
            # Форматируем результат
            if result >= 1000000:
                result_text = f"{result:,.0f}"
            elif result >= 1000:
                result_text = f"{result:,.2f}"
            else:
                result_text = f"{result:.4f}"
            
            self.currency_result.setText(f"{amount} {from_curr} = {result_text} {to_curr}")
            
            # Показываем информацию о курсе и времени обновления
            if REQUESTS_AVAILABLE and self.last_currency_update:
                update_time = self.last_currency_update.strftime("%H:%M:%S")
                self.currency_info.setText(f"Курс: 1 {from_curr} = {rate:.6f} {to_curr}\nОбновлено: {update_time}")
            else:
                self.currency_info.setText(f"Курс: 1 {from_curr} = {rate:.6f} {to_curr}\n(встроенные курсы)")
            
        except ValueError:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Ошибка")
            msg_box.setText("Введите корректную сумму!")
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setStyleSheet(self.styles.get_main_style())
            msg_box.exec_()
        except Exception as e:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Ошибка")
            msg_box.setText(f"Ошибка конвертации: {str(e)}")
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setStyleSheet(self.styles.get_main_style())
            msg_box.exec_()

    def calculate_credit(self):
        """Рассчитывает кредит"""
        try:
            amount = float(self.credit_amount.text())
            rate = float(self.credit_rate.text()) / 100 / 12  # Месячная ставка
            term = int(self.credit_term.text())
            currency = self.credit_currency.currentText()
            
            # Формула аннуитетного платежа
            monthly_payment = amount * (rate * (1 + rate)**term) / ((1 + rate)**term - 1)
            total_payment = monthly_payment * term
            overpayment = total_payment - amount
            
            result = f"Ежемесячный платеж: {monthly_payment:.2f} {currency}\n"
            result += f"Общая сумма выплат: {total_payment:.2f} {currency}\n"
            result += f"Переплата: {overpayment:.2f} {currency}"
            
            self.credit_result.setText(result)
        except ValueError:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Ошибка")
            msg_box.setText("Заполните все поля корректно!")
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setStyleSheet(self.styles.get_main_style())
            msg_box.exec_()

    def calculate_mortgage(self):
        """Рассчитывает ипотеку"""
        try:
            amount = float(self.mortgage_amount.text())
            down_payment = float(self.mortgage_down.text())
            rate = float(self.mortgage_rate.text()) / 100 / 12  # Месячная ставка
            term_years = int(self.mortgage_term.text())
            term_months = term_years * 12
            currency = self.mortgage_currency.currentText()
            
            loan_amount = amount - down_payment
            
            # Формула аннуитетного платежа
            monthly_payment = loan_amount * (rate * (1 + rate)**term_months) / ((1 + rate)**term_months - 1)
            total_payment = monthly_payment * term_months
            overpayment = total_payment - loan_amount
            
            result = f"Сумма кредита: {loan_amount:.2f} {currency}\n"
            result += f"Ежемесячный платеж: {monthly_payment:.2f} {currency}\n"
            result += f"Общая сумма выплат: {total_payment:.2f} {currency}\n"
            result += f"Переплата: {overpayment:.2f} {currency}"
            
            self.mortgage_result.setText(result)
        except ValueError:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Ошибка")
            msg_box.setText("Заполните все поля корректно!")
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setStyleSheet(self.styles.get_main_style())
            msg_box.exec_()

    def calculate_savings(self):
        """Рассчитывает накопления"""
        try:
            monthly = float(self.savings_monthly.text())
            rate = float(self.savings_rate.text()) / 100 / 12  # Месячная ставка
            term_years = int(self.savings_term.text())
            term_months = term_years * 12
            currency = self.savings_currency.currentText()
            
            # Формула будущей стоимости аннуитета
            future_value = monthly * (((1 + rate)**term_months - 1) / rate)
            total_invested = monthly * term_months
            interest_earned = future_value - total_invested
            
            result = f"Ежемесячный взнос: {monthly:.2f} {currency}\n"
            result += f"Общая сумма взносов: {total_invested:.2f} {currency}\n"
            result += f"Накопленная сумма: {future_value:.2f} {currency}\n"
            result += f"Доход от процентов: {interest_earned:.2f} {currency}"
            
            self.savings_result.setText(result)
        except ValueError:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Ошибка")
            msg_box.setText("Заполните все поля корректно!")
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setStyleSheet(self.styles.get_main_style())
            msg_box.exec_()

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