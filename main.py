import os
import sys


def setup_qt_plugins():
    """Настраивает пути к плагинам Qt"""
    if sys.platform.startswith('win'):
        paths = [
            os.path.join(os.path.dirname(__file__), 'PyQt5', 'Qt5', 'plugins'),
            os.path.join(sys.prefix, 'Lib', 'site-packages', 'PyQt5', 'Qt5', 'plugins'),
            os.path.join(sys.prefix, 'Library', 'plugins'),
        ]
    else:
        paths = [
            os.path.join(os.path.dirname(__file__), 'PyQt5', 'Qt5', 'plugins'),
            os.path.join(sys.prefix, 'lib', f'python{sys.version_info.major}.{sys.version_info.minor}',
                         'site-packages', 'PyQt5', 'Qt5', 'plugins'),
            '/usr/lib/x86_64-linux-gnu/qt5/plugins',
            '/usr/lib/qt5/plugins',
            '/usr/lib/qt/plugins',
        ]

    for path in paths:
        platform_path = os.path.join(path, 'platforms')
        if os.path.exists(platform_path):
            os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = platform_path
            return True
    return False


setup_qt_plugins()

from PyQt5.QtWidgets import QApplication
from calculator_ui import MultiCalculator


def main():
    try:
        app = QApplication(sys.argv)
        app.setStyle('Fusion')

        calculator = MultiCalculator()
        calculator.show()

        return_code = app.exec_()
        sys.exit(return_code)

    except Exception as e:
        print(f"Ошибка при запуске: {e}")
        return 1


if __name__ == '__main__':
    main()