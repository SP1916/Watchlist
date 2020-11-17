from django.urls import path
from movies import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin-home', views.admin_home, name='admin-home'),

    path('movietowatch', views.movie_to_watch, name='movietowatch'),
    path('add-movietowatch/<int:pk>', views.add_movietowatch, name='add-movietowatch'),

    path('create/', views.create, name='create'),
    path('update/<int:pk>', views.update, name='update'),
    path('delete/<int:pk>', views.delete, name='delete'),
    path('changeStatus/<int:pk>', views.changeStatus, name='changeStatus'),

]