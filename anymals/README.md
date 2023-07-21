
 <p><center>Anymals </center></p>

Данный проект написан на фрэймворке Django.

Состоит из разделов:News-Promotions(все новости и акции),Cost(размещены продукты,к каждому продукту можно оставить отзыв),Contact(информация о владельцах)


# Установка

### 1) Создать виртуальное окружение
    python3 -m venv venv

    source venv/bin/activate

### 2) Установить зависимости

    pip install -r requirements.txt

### 3) Выполнить миграции

    python manage.py migrate    

### 4) Создать суперпользователя

    python manage.py createsuperuser

# Старт

    python manage.py runserver
