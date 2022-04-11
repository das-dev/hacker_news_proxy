Практические задачки группы Python-04 
=======

## Описание
Прокси сервер, модифицирующий текст на страницах сайта Hacker News следующим образом: после каждого слова из шести букв добавляет значок «™».

## Запуск в Docker
### Собрать контейнер:
```bash
docker build -t proxy .
```
### Запустить тесты:
```bash
docker run -it --rm proxy poetry run pytest
```
### Запустить статический анализ:
```bash
docker run -it --rm proxy poetry run mypy app.py
```
### Запустить сервер:
```bash
docker run -it --rm -p 80:8080 proxy
```

## Запуск в Poetry
### Настроить окружение и зависимости:
```bash
curl -sSL https://install.python-poetry.org | python -
export PATH="$PATH:$HOME/.local/bin"
poetry install
```
### Запустить тесты:
```bash
poetry run pytest
```
### Запустить статический анализ:
```bash
poetry run mypy app.py
```
### Запустить сервер:
```bash
poetry run python app.py
```