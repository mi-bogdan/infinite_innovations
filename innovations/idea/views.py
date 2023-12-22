from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Ip, Topic, Pin, Board, BoardPin, Comments, Like
from django.views.generic.base import View

from .forms import CommentsForms, PinForm, BoardPinForm, BoardForm
from django.contrib.auth.decorators import login_required

from .service import check_user_liked_pin, check_user_board_pin, fancy_line_chart

from django.contrib.auth.models import User

from collections import Counter
import matplotlib.pyplot as plt
from io import BytesIO
import base64


def index(request):
    """Главная страница"""
    context = {
        'title': 'Главная страница'
    }
    return render(request, template_name='idea/index.html', context=context)


def my_view(request):
    # Ваш контекст
    context = {'user': request.user}
    return render(request, 'base.html', context)


class ListPin(ListView):
    """Список идей(pin)"""
    model = Pin
    template_name = 'idea/list.html'
    context_object_name = 'pin_all'
    paginate_by = 4


class DeteilPin(DetailView):
    """Подробная информация о пине"""
    model = Pin
    template_name = 'idea/deteil.html'
    context_object_name = 'pin'
    pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        # Вызываем родительский метод, чтобы получить объект поста
        pin = super().get_object(queryset=queryset)

        # Получаем IP пользователя и добавляем его в просмотры
        ip = self._get_client_ip()
        ip_obj, created = Ip.objects.get_or_create(ip=ip)

        if not pin.views.filter(ip=ip).exists():
            pin.views.add(ip_obj)

        return pin

    def _get_client_ip(self):
        # Получаем IP пользователя через self.request
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pin_id = self.kwargs.get('id')
        user_id = self.request.user.id
        context['is_like'] = check_user_liked_pin(
            self.request, user_id, pin_id)
        context['likes_count'] = Like.objects.filter(pin__id=pin_id).count()
        context['idea'] = Pin.objects.exclude(pk=pin_id)
        context['user_board'] = Board.objects.filter(user__id=user_id)
        context['is_board_pin'] = check_user_board_pin(
            self.request, user_id, pin_id)

        return context


class CommentsAdd(View):
    """Добавление комментария"""

    def post(self, request, id):
        form = CommentsForms(request.POST)
        pin = Pin.objects.get(id=id)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            if request.POST.get('parents', None):
                comment.parents_id = int(request.POST.get('parents'))
            comment.pin = pin
            comment.save()
        return redirect('deteil', pin.id)


def search_by_topic(request):
    """Поиск идей по ТЕМАМ"""
    query = request.GET.get('q')
    if query:
        # Поиск всех тем, содержащих запрос в названии
        topics = Topic.objects.filter(title__icontains=query)
        # Поиск всех идей, связанных с найденными темами
        pins = Pin.objects.filter(topic__in=topics).distinct()
    else:
        pins = Pin.objects.none()

    return render(request, 'idea/search.html', {'pins': pins})


@login_required
def add_pin_view(request):
    """Добавления идеи пользователя"""
    if request.method == 'POST':
        form = PinForm(request.POST, request.FILES,
                       user=request.user)  # Передаём user в форму
        if form.is_valid():
            new_pin = form.save(commit=False)
            new_pin.user = request.user
            new_pin.save()
            form.save_m2m()
            return redirect('index')
    else:
        form = PinForm(user=request.user)
    return render(request, 'idea/add_pin.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class LikeView(View):
    """Добавления лайков к Pin через GET-запрос"""

    def get(self, request, pin_id):
        pin = get_object_or_404(Pin, pk=pin_id)
        like_qs = Like.objects.filter(user=request.user, pin=pin)

        if like_qs.exists():
            like_qs.delete()  # Если лайк уже стоит, удалить его.
        else:
            # Иначе создать лайк.
            Like.objects.create(user=request.user, pin=pin)

        return redirect('deteil', pin_id)


@login_required
def save_pin_view(request, pin_id):
    if request.method == 'POST':
        form = BoardPinForm(request.POST)
        if form.is_valid():
            board_pin = form.save(commit=False)
            board_pin.user_by = request.user
            board_pin.pin = Pin.objects.get(id=pin_id)
            board_pin.save()
        return redirect('deteil', pin_id)


class ListBoard(ListView):
    """Список досок пользователя"""
    model = Board
    template_name = 'idea/user_board.html'
    context_object_name = 'board_all'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('id')
        context['user_board'] = User.objects.get(id=user_id)

        return context

    def get_queryset(self):
        user_id = self.kwargs['id']
        return Board.objects.filter(user__id=user_id)


class BoardPinsListView(ListView):
    model = BoardPin
    template_name = 'idea/board_pins.html'
    context_object_name = 'board_pins'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        board_id = self.kwargs.get('board_id')
        context['boards'] = Board.objects.get(id=board_id)

        return context

    def get_queryset(self):
        bord_id = self.kwargs['board_id']
        return BoardPin.objects.filter(board__id=bord_id)


def create_board(request):
    if request.method == 'POST':
        forms = BoardForm(request.POST)
        if forms.is_valid():
            new_board = forms.save(commit=False)
            new_board.user = request.user
            new_board.save()
        return redirect('add-pin')


@login_required
def delete_board_pin(request, pin_id):
    # Предполагается, что пользователь должен быть вошел в систему для удаления пина
    board_pin = get_object_or_404(
        BoardPin, pin__id=pin_id, user_by=request.user)
    board_pin.delete()
    return redirect('deteil', pin_id)


def generate_histogram(request):
    # Получаем список всех тем
    topics = Topic.objects.all()

    # Подсчитываем количество идей для каждой темы
    topic_counts = Counter(
        Pin.objects.filter(topic__in=topics).values_list(
            'topic__title', flat=True)
    )

    # Теперь можно создать гистограмму с использованием Matplotlib
    plt.figure(figsize=(10, 6))
    plt.bar(topic_counts.keys(), topic_counts.values(), color='skyblue')
    plt.xlabel('Темы')
    plt.ylabel('Количество идей')
    plt.title('Распределение идей по темам')
    # Поворот названий тем для лучшего отображения
    plt.xticks(rotation=45, ha="right")

    # Сохраняем гистограмму в объект BytesIO
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()  # Не забываем закрыть поток после использования

    # Конвертируем BytesIO в строку base64 для встраивания в HTML
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()

    # Передаем данные гистограммы на веб-страницу
    context = {
        'graph': graph,
        'line_chart': fancy_line_chart(request)
    }
    return render(request, 'idea/statistics.html', context)
