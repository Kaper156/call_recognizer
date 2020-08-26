Согласно тестовому заданию в проекте использован **[Tinkoff Voicekit Python client](https://github.com/TinkoffCreditSystems/voicekit_client_python)**
Проект состоит из нескольких частей:
* **cli.py** - обрабатывает аргументы командной строки
* **config.py** - загрузчик конфигурации проекта (ключи **API** и данные для **БД**) 
* **api.py** - клиент использующий **[Tinkoff Voicekit Python client](https://github.com/TinkoffCreditSystems/voicekit_client_python)** для распознования текста
* **analyzer.py** - аналитик транскрипции текста
* **database.py** - клиент базы данных (**Postgres**)
* **logger.py** - настройки логгера проекта
* **helpers.py** - содержит вспомогательные функции 