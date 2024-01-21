# advertising_service

Сервис для публикации объявлений сделанный в качестве тестового задания на вакансию Python Разработчика.

### Стек
- Python 3.11
- FastAPI
- SQLAlchemy
- Alembic

## Запуск проекта

Создайте файл .env в директории /src согласно .env.example.

### Локальный запуск.
Создайте окружение.

```bash
py -3.11 -m venv venv
```

Запустите окружение.

```bash
source venv/Scripts/activate
```

И установите необходимые библиотеки.

```bash
pip install -r requirements.txt
```

Необходимо перейти в директорию src и выполнить main.py файл.

```bash
cd src/
```

```bash
python main.py
```

main.py принимает несколько параметров: --port --host.

```bash
python main.py --host 0.0.0.0 --port 8080
```

Проект запущен (стандартный ip http://127.0.0.1:8000)

Так же main.py принимает команду create_superuser, для создания в БД юзера с правами администратора.

```bash
python main.py create_superuser
```

Данный запуск требует настройку PostgreSQL

### Запуск в Docker контейнерах.

Перейдите в директорию /infra и запустите контейнеры при помощи команды

```bash
docker-compose up -d # Для win
sudo docker-compose up -d # Для linux
```

Проект запущен и доступен по http://127.0.0.1:80 или http://localhost:80.

### Выполнение миграций

Для того, чтобы миграции были применены необходимо выполнить команду

```bash
alembic upgrade ccfaf60db433 # локальный запуск из src
docker-compose exec -T backend alembic upgrade ccfaf60db433 # контейнер win
sudo docker-compose exec -T backend alembic upgrade ccfaf60db433 # контейнер linux
```

## Документация

Документация находить в директории docs в формате OpenAPI

Если проект запущен доступна динамическая swagger документация по: 
- http://127.0.0.1:8000/docs локальный запуск
- http://127.0.0.1:80/docs запуск в контейнере 

Автор [Воложанин Пётр](https://github.com/V1cimus)

