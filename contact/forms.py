from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from . import models


class ContactForm(forms.ModelForm):
    picture = forms.ImageField(
        label='Изображение',
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*',
                # Эта строка указывает, что принимаются любые изображения. Можно ограничить, если нужно.
            }
        ),
        required=False,  # Необязательно добавлять изображение
    )

    class Meta:
        model = models.Contact
        fields = (
            'first_name', 'last_name', 'phone', 'email', 'description',
            'category', 'picture'
        )
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "email": "Электронная почта",
            "phone": "Телефон",
            "description": "Описание",
            "category": "Категория",
            "picture": "Изображение"
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if first_name == last_name:
            msg = ValidationError(
                'Фамилия не может быть одинаковой с именем',
                code='invalid'
            )
            self.add_error('last_name', msg)

        return super().clean()

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if first_name == 'ABC':
            self.add_error(
                'first_name',
                ValidationError(
                    'Ошибка из метода add_error', code='invalid'
                )
            )

        return first_name


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label='Имя',
        required=True,
        min_length=3,
    )

    last_name = forms.CharField(
        label='Фамилия',
        required=True,
        min_length=3,
    )

    email = forms.EmailField()

    # Эти поля (first_name, last_name, email) обязаны быть заполнены пользователем.
    # Без них пользователи могут не указать эти данные.
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'username', 'password1',
            'password2',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():  # Если существует пользователь с таким email, возвращает TRUE
            self.add_error(
                'email',
                ValidationError('Этот email уже существует', code='invalid')
            )

        return email


class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Имя',
        min_length=2,
        max_length=30,
        required=True,
        help_text='Обязательно.',
        error_messages={
            'min_length': 'Пожалуйста, введите более 2 символов.'
        }
    )

    last_name = forms.CharField(
        label='Фамилия',
        min_length=2,
        max_length=30,
        required=True,  # Для обязательности заполнения
        help_text='Обязательно.',
    )

    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        # Для отображения подсказок по заполнению пароля
        required=False,
    )

    password2 = forms.CharField(
        label='Пароль (повторите)',
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text='Используйте тот же пароль, что и ранее.',
        required=False,
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'username',
        )

    # Эта функция сохраняет пароль в базе данных, чтобы он был зашифрован
    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)

        password = self.cleaned_data.get('password1')

        if password:
            user.set_password(password)  # Метод 'set_password' используется для сохранения пароля в зашифрованном виде.

        if commit:
            user.save()

        return user

    # Эта функция проверяет, совпадают ли два пароля
    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:  # Если хотя бы один из паролей был изменен
            if password1 != password2:  # Проверка на совпадение паролей
                self.add_error('password2',
                               ValidationError('Пароли не совпадают'))  # Сообщение об ошибке, если пароли не совпадают

        return super().clean()

        # Эта функция проверяет, был ли изменен email, и если был — не существует ли уже такого email у другого пользователя

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email

        if current_email != email:  # Это означает, что пользователь хочет изменить email, тогда...
            if User.objects.filter(
                    email=email).exists():  # Если существует другой пользователь с таким email, то возвращает TRUE
                self.add_error(
                    'email',
                    ValidationError('Этот email уже существует', code='invalid')
                )

        return email

    # Эта функция проверяет, был ли изменен пароль и валиден ли он
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1:  # Если введен новый пароль
            try:
                password_validation.validate_password(password1)  # Проверка пароля на валидность
            except ValidationError as errors:  # Если есть ошибки, они обрабатываются
                self.add_error('password1', ValidationError(errors))  # Ошибки отображаются под полем пароля

        return password1
