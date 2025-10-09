import math
import re


class CalculatorEngine:
    """Математическое ядро калькулятора"""

    def __init__(self):
        self.safe_dict = {
            'math': math,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'log': math.log10,
            'ln': math.log,
            'sqrt': math.sqrt,
            'pi': math.pi,
            'e': math.e,
            '__builtins__': {}
        }

    def safe_eval(self, expression):
        """Безопасное вычисление математического выражения"""
        try:
            if not expression.strip():
                return 0

            expr = self.prepare_expression(expression)

            if not self.is_expression_safe(expr):
                raise ValueError("Недопустимые символы в выражении")

            result = eval(expr, {"__builtins__": {}}, self.safe_dict)
            result = self.process_result(result)

            return result

        except ZeroDivisionError:
            raise ValueError("Деление на ноль")
        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Ошибка вычисления: {str(e)}")

    def prepare_expression(self, expression):
        """Подготавливает выражение для вычисления"""
        expr = expression

        # Базовые замены
        replacements = {
            'π': 'pi',
            '√': 'sqrt',
            '×': '*',
            '÷': '/',
            'x^y': '**',
            '^': '**',
        }

        for old, new in replacements.items():
            expr = expr.replace(old, new)

        # Обрабатываем x²
        expr = re.sub(r'(\d+(?:\.\d+)?)x²', r'(\1**2)', expr)
        if expr.endswith('x²'):
            expr = expr[:-2] + '**2'

        # Обрабатываем функции
        func_patterns = [
            (r'sin(\d+(?:\.\d+)?)', r'sin(\1)'),
            (r'cos(\d+(?:\.\d+)?)', r'cos(\1)'),
            (r'tan(\d+(?:\.\d+)?)', r'tan(\1)'),
            (r'log(\d+(?:\.\d+)?)', r'log(\1)'),
            (r'ln(\d+(?:\.\d+)?)', r'ln(\1)'),
            (r'sqrt(\d+(?:\.\d+)?)', r'sqrt(\1)'),
        ]

        for pattern, replacement in func_patterns:
            expr = re.sub(pattern, replacement, expr)

        return expr

    def is_expression_safe(self, expression):
        """Проверяет выражение на безопасность"""
        allowed_chars = set('0123456789.+-*/() abcdefghijklmnopqrstuvwxyz_')
        return all(c in allowed_chars for c in expression.lower())

    def process_result(self, result):
        """Обрабатывает результат вычисления"""
        if math.isnan(result):
            raise ValueError("Результат неопределен")
        if math.isinf(result):
            raise ValueError("Результат бесконечен")

        if isinstance(result, float):
            if result == 0.0:
                result = 0.0
            else:
                result = round(result, 10)
                if result == int(result):
                    result = int(result)

        return result