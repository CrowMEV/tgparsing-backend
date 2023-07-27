# tgparsing-backend

## Клонирование и настройка проекта

### HTTPS
```bash
git clone https://github.com/CrowMEV/tgparsing-backend.git tgparsing
```

### SSH
```bash
git clone git@github.com:CrowMEV/tgparsing-backend.git tgparsing
```

## Локальный запуск сервера

### Переход в директорию, установка пакетов и накат миграций
**Для запуска сервера переменные окружения не нужны. Данные для базы данных можно взять из файла settings. До запуска миграций база данных должна быть уже создана**
```bash
cd tgparsing
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip -r requirements.txt
poetry install

```
### Запуск docker compose с базой для разработки
Переименовавать файл env.example в .env, пустые ключи заполнить согласно settings.py дефолтными значения
Запустить docker compose
```bash
docker compose up -d
```
### Установка pre-commit hooks

Установка хуков
```bash
pre-commit install
```
Для того чтобы прогнать тест по всему коду, а не только по коммиту
```bash
pre-commit run --all-files
```

### Загрузка ролей в базу данных
```bash
alembic upgrade head
./manage.py db load-roles roles_data.json
```

### Запуск тестов
```bash
poetry run pytest
```
### Запуск сервера

```bash
./manage.py site run
```
### Для очистки контейнеров
```bash
docker compose down -v
```

Документация:  
- [Swagger](http://0.0.0.0:8000/docs)  
- [Redoc](http://127.0.0.1:8000/redoc)  

#### Примечание  
В качестве логина используется e-mail  
