from django.contrib import admin
from contact import models


# Регистрируем модели в админке
@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = 'id', 'first_name', 'last_name', 'email', 'phone', 'show',
    ordering = '-id',  # Сортировка по убыванию id
    search_fields = 'id', 'first_name', 'last_name',  # Поиск по этим полям
    list_per_page = 10  # Количество элементов на странице
    list_max_show_all = 100  # Максимальное количество элементов, которые можно показать
    list_display_links = 'first_name', 'last_name', 'email', 'phone',  # Ссылки на поля для редактирования
    list_editable = 'show',  # Поле 'show' будет доступно для быстрого редактирования


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'name',  # Отображение только поля 'name' в списке
    ordering = 'id',  # Сортировка по id по возрастанию
