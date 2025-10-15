import math
import re
import ast
import operator


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
            'exp': math.exp,
            'abs': abs,
            'factorial': math.factorial,
            'cbrt': lambda x: x**(1/3) if x >= 0 else -(-x)**(1/3),
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

        # Обрабатываем факториал
        expr = re.sub(r'(\d+(?:\.\d+)?)!', r'factorial(int(\1))', expr)

        # Обрабатываем функции - функции уже имеют скобки из UI
        # Дополнительная обработка не требуется, так как UI добавляет скобки автоматически

        return expr

    def is_expression_safe(self, expression):
        """Проверяет выражение на безопасность"""
        allowed_chars = set('0123456789.+-*/() abcdefghijklmnopqrstuvwxyz_!')
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


class StepByStepSolver:
    """Класс для пошагового решения математических выражений"""
    
    def __init__(self):
        self.steps = []
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
    
    def solve_step_by_step(self, expression):
        """Решает выражение пошагово и возвращает объяснение"""
        self.steps = []
        self.step_counter = 0  # Счетчик для математических шагов
        try:
            # Подготавливаем выражение
            prepared_expr = self.prepare_expression(expression)
            self.steps.append(f"Исходное выражение: {expression}")
            self.steps.append(f"Подготовленное выражение: {prepared_expr}")
            
            # Парсим и решаем пошагово
            result = self.evaluate_expression(prepared_expr)
            
            self.steps.append(f"Ответ: {result}")
            return result, self.steps
            
        except Exception as e:
            self.steps.append(f"Ошибка: {str(e)}")
            return None, self.steps
    
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
        
        return expr
    
    def evaluate_expression(self, expr):
        """Рекурсивно вычисляет выражение пошагово"""
        try:
            # Парсим выражение в AST
            tree = ast.parse(expr, mode='eval')
            return self.evaluate_node(tree.body)
        except Exception as e:
            raise ValueError(f"Ошибка парсинга: {str(e)}")
    
    def evaluate_node(self, node):
        """Рекурсивно вычисляет узел AST"""
        if isinstance(node, ast.Constant):  # Число
            return node.value
        elif isinstance(node, ast.Name):  # Переменная (pi, e, функции)
            if node.id in self.safe_dict:
                return self.safe_dict[node.id]
            else:
                raise ValueError(f"Неизвестная переменная: {node.id}")
        elif isinstance(node, ast.BinOp):  # Бинарная операция
            left = self.evaluate_node(node.left)
            right = self.evaluate_node(node.right)
            
            # Получаем оператор
            op_func = self.get_operator_function(node.op)
            op_symbol = self.get_operator_symbol(node.op)
            
            # Формируем шаг
            left_str = self.format_value(left)
            right_str = self.format_value(right)
            result = op_func(left, right)
            result_str = self.format_value(result)
            
            self.step_counter += 1
            step = f"Шаг {self.step_counter}: {left_str} {op_symbol} {right_str} = {result_str}"
            self.steps.append(step)
            
            return result
        elif isinstance(node, ast.UnaryOp):  # Унарная операция
            operand = self.evaluate_node(node.operand)
            if isinstance(node.op, ast.USub):  # Минус
                result = -operand
                self.step_counter += 1
                step = f"Шаг {self.step_counter}: -{self.format_value(operand)} = {self.format_value(result)}"
                self.steps.append(step)
                return result
        elif isinstance(node, ast.Call):  # Функция
            func_name = node.func.id if hasattr(node.func, 'id') else str(node.func)
            args = [self.evaluate_node(arg) for arg in node.args]
            
            if func_name in self.safe_dict:
                func = self.safe_dict[func_name]
                result = func(*args)
                args_str = ', '.join(self.format_value(arg) for arg in args)
                result_str = self.format_value(result)
                self.step_counter += 1
                step = f"Шаг {self.step_counter}: {func_name}({args_str}) = {result_str}"
                self.steps.append(step)
                return result
            else:
                raise ValueError(f"Неизвестная функция: {func_name}")
        else:
            raise ValueError(f"Неподдерживаемый тип узла: {type(node)}")
    
    def get_operator_function(self, op):
        """Возвращает функцию оператора"""
        operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.Mod: operator.mod,
        }
        return operators.get(type(op), operator.add)
    
    def get_operator_symbol(self, op):
        """Возвращает символ оператора"""
        symbols = {
            ast.Add: '+',
            ast.Sub: '-',
            ast.Mult: '*',
            ast.Div: '/',
            ast.Pow: '^',
            ast.Mod: '%',
        }
        return symbols.get(type(op), '+')
    
    def format_value(self, value):
        """Форматирует значение для отображения"""
        if isinstance(value, float):
            if value == int(value):
                return str(int(value))
            else:
                return f"{value:.6g}"
        return str(value)