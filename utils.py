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

def format_number(number):
    """Форматирует число для отображения"""
    if isinstance(number, float):
        if number.is_integer():
            return str(int(number))
        # Ограничиваем количество знаков после запятой
        return f"{number:.10g}"
    return str(number)