from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.user_profile, name='profile'),
    path('room/<int:room_id>/', views.room_detail, name='room_detail'),
    path('book/<int:room_id>/', views.book_room, name='book_room'),
    path('bookings/', views.my_bookings, name='my_bookings'),
    path('pay/<int:booking_id>/', views.make_payment, name='make_payment'),
    path('logout/', views.logout_view, name='logout'),
]
