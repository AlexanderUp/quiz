# Сервис автоматического тестирования

## Описание

Сервис позволяет проходить тестирование по сгруппированным по темам вопросам с последующим объявлением результатов тестирования.

## Функциональные части сервиса:

Реализован следующий функционал приложения:
- Регистрация новых пользователей;
- Аутентификация зарегистрированных пользователей;
- Прохождение любого набора тестовых вопросов зарегистрированными пользователями;
- Требование последовательного ответа на все вопросы, каждый вопрос выводится на новой странице (перескакивать через вопросы или оставлять их неотвеченными нельзя);
- После завершения тестирования сообщается результат:
    - количество правильных/неправильных ответов;
    - процент правильных ответов.
- Админка. Стандартная админка Django. Разделы:
    - Стандартный раздел пользователей;
    - Раздел с наборами тестов с возможностью добавлять в них вопросы;
    - Возможность на странице набора вопросов добавлять ответы к ним (с указанием правильных вариантов ответа);
    - Валидация на то, что должен быть хотя бы 1 правильный вариант;
    - Валидация на то, что все варианты не могут быть правильными;
    - Удаление вопросов/вариантов ответов/изменение правильных решений при редактировании тестового набора.
- Наполнение базы данных заранее сформированными вопросами из csv-файла.


## Список основных моделей в БД

- Модель типа вопроса карт со следующими полями:
    - название типа вопроса;
    - описание типа вопроса.

- Модель вопроса со следующими полями:
    - тип вопроса;
    - описание вопроса.

- Модель ответа на вопрос со следующими полями:
    - внешний ключ связанного вопроса;
    - описание ответа;
    - указание, является ли ответ верным.


## Запуск приложения:

- Клонирование репозитория:

```https://github.com/AlexanderUp/quiz.git```

- Переход в корневую папку проекта:

```cd quiz```

- Создание виртуального окружения:

```python -m venv venv```

- Активация виртуального окружения (macOS):

```source venv/bin/activate```

- Переход в папку 'quiz':

```cd quiz```

- Создание и применение миграций:

```python manage.py makemigrations```

```python manage.py migrate```

- Создание суперпользователя (для доступа в административную часть приложения):

```python manage.py createsuperuser```

- Наполнение БД вопросами из подготовленных данных.

```python manage.py populate_db```

- Запуск сервера:

```python manage.py runserver```
