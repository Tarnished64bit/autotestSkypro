## Тестирование Читай-город

# Установка зависимостей
pip install -r requirements.txt

# Запуск всех тестов
pytest -v

# Запуск API тестов
pytest test_api.py -v

# Запуск UI тестов
pytest test_ui.py -v
