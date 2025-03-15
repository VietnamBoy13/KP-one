import os
import sys
from datetime import datetime
from pathlib import Path
from random import choice

import django
from django.conf import settings

DJANGO_BASE_DIR = Path(__file__).parent.parent  # перемещаемся на уровень выше, чтобы Django искал вещи, которые не находятся внутри этой модели
NUMBER_OF_OBJECTS = 1000  # количество объектов, которые должны быть созданы

sys.path.append(str(DJANGO_BASE_DIR))
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
settings.USE_TZ = False  # чтобы игнорировать ошибку с часовыми поясами, чтобы не было конфликта с временной зоной

django.setup()  # Инициализация Django.

if __name__ == '__main__':  # Начало моего скрипта
    import faker  # Эта библиотека используется для генерации фальшивых данных, которые могут быть использованы для тестирования приложения

    from contact.models import Category, Contact

    # Эти два метода ниже удаляют все контакты, созданные в базе данных, перед добавлением фальшивых данных. Я их закомментировал, чтобы не удалять данные.
    # Contact.objects.all().delete()
    # Category.objects.all().delete()

    fake = faker.Faker('en-us')  # Для генерации имен на английском. Для Бразилии будет 'pt_br'.
    categories = ['Amigo(a)', 'Família', 'Colega']  # Категории должны быть уже созданы в админке Django

    django_categories = [Category(name=name) for name in categories]  # Используем list comprehension для создания категорий

    for category in django_categories:
        category.save()  # Сохраняем категории в базе данных

    django_contacts = []

    for _ in range(NUMBER_OF_OBJECTS):
        profile = fake.profile()  # Генерируем профиль с различными данными
        email = profile['mail']  # Извлекаем email
        first_name, last_name = profile['name'].split(' ', 1)  # Извлекаем первое и последнее имя
        phone = fake.phone_number()  # Генерируем номер телефона
        created_date: datetime = fake.date_this_year()  # Генерируем дату, только этого года
        description = fake.text(max_nb_chars=100)  # Генерируем текст длиной до 100 символов для описания
        category = choice(django_categories)  # Случайным образом выбираем одну из категорий

        # Добавляем данные в список контактов
        django_contacts.append(
            Contact(
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                created_date=created_date,
                description=description,
                category=category,
            )
        )

    if len(django_contacts) > 0:  # Проверяем, если список django_contacts не пуст
        Contact.objects.bulk_create(django_contacts)  # Создаем и сохраняем все объекты в базе данных за один раз
