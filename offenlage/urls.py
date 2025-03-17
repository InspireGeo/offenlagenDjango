from django.contrib import admin
from django.urls import path
from . import views



app_name = "offenlage"

urlpatterns = [
    path('', views.index, name='index'),  # Ana sayfa
    path('offenlagedashboard/', views.offenlagedashboard, name="offenlagedashboard"),
    path('addoffenlage/', views.addoffenlage, name="addoffenlage"),
    path('offenlage/<int:id>', views.detailOffenlage, name="detailOffenlage"),
    path('offenlageupdate/<int:id>', views.updateOffenlage, name="offenlageupdate"),
    path('offenlagedelete/<int:id>', views.deleteOffenlage, name="offenlagedelete"),  # Silme URL'si
    path('about/', views.about, name='about'),  # Hakkında sayfası için URL
]
