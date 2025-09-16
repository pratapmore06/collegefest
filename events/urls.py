from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # this is for '/'
    path('events/', views.home, name='events_list'),  # add this line
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('participate/<int:event_id>/', views.participate_event, name='participate_event'),
     path('my-participations/', views.my_participations, name='my_participations'),
    path('participation/<int:pk>/edit/', views.edit_participation, name='edit_participation'),
    path('participation/<int:pk>/delete/', views.delete_participation, name='delete_participation'),

]
