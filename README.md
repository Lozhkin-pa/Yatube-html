# Yatube
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white) ![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white)

Проект Yatube — это платформа для публикаций, блог. У пользователей есть возможность публиковать и управлять записями, просматривать чужие записи.

### __Возможности__
- создать свою страницу;
- создать/изменить запись;
- зайти на чужую страницу и посмотреть все записи автора;
- посмотреть все записи всех авторов;
- подписаться на избранных авторов;
- смотреть публикации только избранных авторов;
- автор может выбрать имя и уникальный адрес для своей страницы;

### __Установка на локальном компьютере__
1. Клонируйте репозиторий
```
> git clone git@github.com:Lozhkin-pa/yatube.git
```
2. Установите и активируйте виртуальное окружение
```
> python -m venv venv
> source venv/Scripts/activate  - для Windows
> source venv/bin/activate - для Linux
```
3. Установите зависимости
```
> python -m pip install --upgrade pip
> pip install -r requirements.txt
```
4. Перейти в папку yatube и выполнить миграции
```
> cd yatube/
> python manage.py migrate
```
4. Запустите проект
```
> python manage.py runserver
```

### __Технологии__
* [Python 3.2.0](https://www.python.org/doc/)
* [Django 2.2.16](https://docs.python-telegram-bot.org/en/v20.7/)
* [Pytest 6.2.4](https://docs.pytest.org/en/7.1.x/contents.html)
* [Pytest-django 4.4.0](https://pytest-django.readthedocs.io/en/latest/)
* [requests 2.26.0](https://requests.readthedocs.io/en/latest/)
* [Pillow 6.2.4](https://pillow.readthedocs.io/en/stable/)

### __Автор__
[Павел Ложкин](https://github.com/Lozhkin-pa)
