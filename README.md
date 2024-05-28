[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=29&pause=1000&color=2336BCF7&width=435&lines=YaMDb+API+Yatube)](https://git.io/typing-svg)
[![Python](https://img.shields.io/badge/-Python-464641?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-464646?style=flat-square&logo=django)](https://www.djangoproject.com/)
[![Postman](https://img.shields.io/badge/Postman-464646?style=flat-square&logo=postman)](https://www.postman.com/)

### Яндекс Практикум. Спринт 10. Проект YaMDb (групповой проект).

## Описание  
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Title).
Произведения делятся на категории: «Книги», «Фильмы», «Музыка».
Список категорий (Category) может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха. Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.

Благодарные или возмущённые читатели оставляют к произведениям текстовые отзывы (Review) и выставляют произведению рейтинг (оценку в диапазоне от одного до десяти). Из множества оценок автоматически высчитывается средняя оценка произведения.

Полная документация к API находится по эндпоинту /redoc

## Стек технологий :
- Python
- Django
- Django REST Framework
- REST API
- SQLite
- Аутентификация по JWT-токену


## Ресурсы API YaMDb
**USERS**: пользователи.

**AUTH**: аутентификация.

**TITLES**: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).

**CATEGORIES**: категории (типы) произведений ("Фильмы", "Книги", "Музыка").

**GENRES**: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.

**REVIEWS**: отзывы на произведения. Отзыв привязан к определённому произведению.

**COMMENTS**: комментарии к отзывам. Комментарий привязан к определённому отзыву.

## Как запустить проект:

1. Клонировать репозиторий
```
    git clone git@github.com:DvGreeN/api_yamdb.git
```
2. Развернуть в репозитории виртуальное окружение
```
    python -m venv venv
```
3. Запустить виртуальное окружение
```
    source venv/Scripts/activate
``` 
4. Установить зависимости в виртуальном окружении
```
    pip install -r requirements.txt
```
5. Выполнить миграции
```
    python manage.py makemigrations
```
```
    python manage.py migrate
```
6. Импорт тестовых данных
```
    python manage.py import_csv
```

7. Запустить проект
```
    python manage.py runserver
```

## Авторы: 

- 👋 [Anna-Karpov-A](https://github.com/Anna-Karpov-A) - Auth/Users  
- 👋 [DvGreeN](https://github.com/DvGreeN) - Categories/Genres/Titles/Импорт данных из csv файлов  
- 👋 [Etl0n](https://github.com/Etl0n) - Review/Comments  

