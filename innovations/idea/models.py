from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def file_validator(value):
    import os
    from django.core.files.images import get_image_dimensions
    ext = os.path.splitext(value.name)[1]  # Получаем расширение файла
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mov', '.avi']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Неподдерживаемое расширение файла.')


def validate_file_type(upload):
    import magic
    file_type = magic.from_buffer(upload.file.read(2048), mime=True)
    upload.file.seek(0)
    if not (file_type.startswith('image/') or file_type.startswith('video/')):
        raise ValidationError('Этот тип файла не поддерживается.')


class Ip(models.Model):  # таблица где будут айпи адреса
    """Айпи адреса"""
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = "Ip"
        verbose_name_plural = "Ip"
        db_table = "ip"


class Topic(models.Model):
    """Тема"""
    title = models.CharField(verbose_name='Тема', max_length=100)
    create_at = models.DateTimeField(
        verbose_name="Дата темы", auto_now_add=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Темы"
        db_table = "tipic"


class Board(models.Model):
    """Доска"""
    title = models.CharField(verbose_name='Заголовок', max_length=100)
    description = models.TextField(
        verbose_name='Описание', blank=True, null=True)
    user = models.ForeignKey(
        User, verbose_name='Пользователь', on_delete=models.CASCADE)
    create_at = models.DateTimeField(
        verbose_name="Дата публикации", auto_now_add=True)
    update_at = models.DateTimeField(
        verbose_name="Дата обновления", auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Доска"
        verbose_name_plural = "Доски"
        db_table = "board"


class Pin(models.Model):
    """Идея"""
    title = models.CharField(verbose_name='Заголовок',
                             max_length=250, blank=True, null=True)
    description = models.TextField(
        verbose_name='Описание', blank=True, null=True)
    create_at = models.DateTimeField(
        verbose_name="Дата публикации", auto_now_add=True)
    update_at = models.DateTimeField(
        verbose_name="Дата обновления", auto_now=True)
    topic = models.ManyToManyField(Topic, verbose_name='Темы')
    views = models.ManyToManyField(Ip, related_name='pin_views', blank=True)
    idea = models.FileField(verbose_name='Идея', upload_to='media/',
                            validators=[file_validator, validate_file_type])
    board = models.ForeignKey(Board, on_delete=models.CASCADE, verbose_name='Основная доска',
                              related_name='original_pins')  # основная доска для Pin
    user = models.ForeignKey(
        User, verbose_name='Пользователь', on_delete=models.CASCADE)

    def is_image(self):
        return self.idea and any(self.idea.name.lower().endswith(image) for image in ['.jpg', '.jpeg', '.png', '.gif'])

    def is_video(self):
        return self.idea and any(self.idea.name.lower().endswith(video) for video in ['.mp4', '.mov', '.avi'])

    def get_reviews(self):
        return self.comments_set.filter(parents__isnull=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Идея"
        verbose_name_plural = "Идеи"
        db_table = "pin"


class BoardPin(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, verbose_name='Доска',
                              related_name='pinned_pins')  # доска, куда пин был закреплен
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE,
                            verbose_name='Идея', related_name='saves')
    # пользователь, который добавил пин на доску
    user_by = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Кем добавлено')
    create_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return f"{self.board.title} - {self.pin.title}"

    class Meta:
        verbose_name = "Закрепление Идеи на Доске"
        verbose_name_plural = "Закрепления Идей на Досках"
        db_table = "board_pin"
        constraints = [
            models.UniqueConstraint(
                fields=['board', 'pin'], name='unique_pin_on_board')
        ]


class Comments(models.Model):
    """Комментарий"""

    text = models.TextField(verbose_name="Отписание", max_length=5000)
    user = models.ForeignKey(
        User, verbose_name='Пользователь', on_delete=models.CASCADE)
    parents = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True)
    pin = models.ForeignKey(
        Pin, verbose_name="Идея", on_delete=models.CASCADE)
    create_at = models.DateTimeField(
        verbose_name="Дата отзыва", auto_now_add=True, null=True)

    def __str__(self) -> str:
        return f"{self.user}-{self.pin}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        db_table = "comments"


class Like(models.Model):
    """Лайки"""
    user = models.ForeignKey(
        User, verbose_name='Пользователь', on_delete=models.CASCADE)
    pin = models.ForeignKey(
        Pin, verbose_name='Идея', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user}-{self.pin}'

    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"
        db_table = "like"
