# Джанго
## Шаблон бэка форума

### Установка

#### 1) Первые шаги
    Склонить репозиторий
    Прописать свое подключение к БД в local_settings.py
  
#### 2) Создать виртуальное окружение
    python -m venv venv

#### 3) Активировать виртуальное окружение
    . venv/bin/activate
   
#### 4) Установить зависимости:
    pip install -r req.txt

#### 5) Выполнить команду для выполнения миграций
    python manage.py migrate

#### 6) Создать суперпользователя
    python manage.py createsuperuser

#### 7) Запустить сервер
    python manage.py runserver
