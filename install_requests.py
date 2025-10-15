#!/usr/bin/env python3
"""
Скрипт для установки библиотеки requests
"""
import subprocess
import sys

def install_requests():
    """Устанавливает библиотеку requests"""
    try:
        print("Устанавливаем библиотеку requests...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        print("✅ Библиотека requests успешно установлена!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка установки: {e}")
        return False
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        return False

if __name__ == "__main__":
    if install_requests():
        print("\n🎉 Теперь можно запускать калькулятор с конвертацией валют!")
        print("Запустите: python main.py")
    else:
        print("\n💡 Попробуйте установить вручную:")
        print("pip install requests")
