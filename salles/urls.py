# salles/urls.py
from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.liste_salles, name='liste_salles'),
    path('<int:salle_id>/', views.detail_salle, name='detail_salle'),

]