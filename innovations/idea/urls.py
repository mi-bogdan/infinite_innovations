from django.urls import path
from .views import index, ListPin, DeteilPin, CommentsAdd, search_by_topic, add_pin_view, LikeView, save_pin_view, ListBoard, BoardPinsListView, create_board, delete_board_pin, generate_histogram


urlpatterns = [
    path('', index, name='index'),
    path('list/', ListPin.as_view(), name='list'),
    path('deteil/<id>/', DeteilPin.as_view(), name='deteil'),
    path('comments-add/<id>/', CommentsAdd.as_view(), name='comments-add'),
    path('search/', search_by_topic, name='search'),
    path('add-pin/', add_pin_view, name='add-pin'),
    path('like/<pin_id>/', LikeView.as_view(), name='like'),
    path('save_pin/<int:pin_id>/', save_pin_view, name='save_pin'),
    path('list_board/<int:id>/', ListBoard.as_view(), name='list_board'),
    path('board/<int:board_id>/pins/',
         BoardPinsListView.as_view(), name='board_pins'),
    path('board-add/', create_board, name='board-add'),
    path('delete_board_pin/<int:pin_id>/',
         delete_board_pin, name='delete_board_pin'),
    path('statistics', generate_histogram, name='statistics'),
 
]
