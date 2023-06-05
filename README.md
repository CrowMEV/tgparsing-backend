# tgparsing-backend

## Клонирование и настройка проекта

### HTTPS
```bash
git clone https://github.com/CrowMEV/tgparsing-backend.git tgparsing
cd tgparsing
python3 -m venv venv
source venv/bin/activate
```

### SSH
```bash
git clone git@github.com:CrowMEV/tgparsing-backend.git tgparsing
cd tgparsing
python3 -m venv venv
source venv/bin/activate
```

## Локальный запуск сервера

### Переход в директорию, установка пакетов и накат миграций
**Для запуска сервера переменные окружения не нужны. Данные для базы данных можно взять из файла settings. До запуска миграций база данных должна быть уже создана**
```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
```
### Загрузка ролей в базу данных
```bash
./manage.py db load-roles roles_data.json
```
### Запуск тестов
```bash
pytest
```
### Запуск сервера

```bash
./manage.py site run
```

### Форматирование кода
Прежде чем добавлять и коммитить файлы, необходимо привести код к определенному стандарту. Для этого выполните команду ниже:
```bash
python3 -m black .
```
or
```bash
black .
```

Документация:  
- [Swagger](http://0.0.0.0:8000/docs)  
- [Redoc](http://127.0.0.1:8000/redoc)  

#### Примечание  
В качестве логина используется e-mail  
