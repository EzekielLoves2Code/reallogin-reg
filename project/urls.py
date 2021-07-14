from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('registration', views.regis),
    path('login', views.login),
    path('ideas', views.show_all),
    path('logout', views.logout),
    path('create', views.createidea),
    path('<int:idea_id>', views.idea),
    path('<int:idea_id>/edit', views.edit),
    path('createpage', views.newidea),
    path('<int:idea_id>/editpage', views.editpage),
    path('<int:idea_id>/remove', views.remove),
    path('<int:idea_id>/like', views.add_like),
]