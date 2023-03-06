from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.home_page_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/<int:pk>/',views.UserDetailView.as_view(),name='user_detail'),
    path('users-list/',views.UserListView.as_view(), name='users_list'),
    path('about/',views.about_us_page_view, name='about_us'),
    path('contact/',views.contact_us_page_view, name='contact_us'),
    ]