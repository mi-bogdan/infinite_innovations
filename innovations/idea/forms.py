from django import forms
from .models import Comments, Pin, Board, BoardPin


class CommentsForms(forms.ModelForm):
    """Форма отзыва"""
    class Meta:
        model = Comments
        fields = ['text']


class PinForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Получаем пользователя из kwargs
        super(PinForm, self).__init__(*args, **kwargs)
        if self.user:  # Если пользователь задан, ограничиваем набор досок
            self.fields['board'].queryset = Board.objects.filter(
                user=self.user)

    class Meta:
        model = Pin
        fields = ['title', 'description', 'topic', 'idea', 'board']


class BoardPinForm(forms.ModelForm):
    class Meta:
        model = BoardPin
        fields = ['board']


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'description']
     
