from .models import Like, BoardPin, Comments, Pin


from django.db.models.functions import TruncDay
import matplotlib.pyplot as plt
from io import BytesIO
from matplotlib.dates import DateFormatter
import base64

import matplotlib.dates as mdates
from django.db import models

def check_user_liked_pin(request, user_id, pin_id):
    """Проверка, поставил ли пользователь 'user_id' лайк на пин 'pin_id'."""
    if request.user.is_authenticated:
        user_has_liked = Like.objects.filter(
            user__id=user_id, pin__id=pin_id).exists()
        return user_has_liked
    else:
        return False


def check_user_board_pin(request, user_id, pin_id):
    """Проверка, добавил ли пользователь к доске пин."""
    if request.user.is_authenticated:
        user_has_board = BoardPin.objects.filter(
            user_by__id=user_id, pin__id=pin_id).exists()
        return user_has_board
    else:
        return False


def fancy_line_chart(request):
    # Собираем данные
    pin_comments = Comments.objects.annotate(date=TruncDay('create_at')).values('date').annotate(count=models.Count('id')).order_by('date')
    
    dates = [comment['date'] for comment in pin_comments]
    comment_counts = [comment['count'] for comment in pin_comments]

    # Создаем график
    plt.figure(figsize=(10, 5))
    
  
    plt.plot_date(dates, comment_counts, linestyle='-', linewidth=2, marker='o', color='dodgerblue', markersize=5, label='Количество комментариев')
    plt.gcf().autofmt_xdate()
    date_format = DateFormatter('%Y-%m-%d')
    plt.gca().xaxis.set_major_formatter(date_format)
    
    # Дополнительные настройки графика
    plt.grid(True)
    plt.legend()
    plt.xlabel('Дата')
    plt.ylabel('Количество комментариев')
    plt.title('Динамика комментариев по дням')
    plt.tight_layout()

    # Сохраняем график в PNG-изображение
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Конвертируем PNG-изображение в строку base64 для вставки в HTML
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    return graphic
