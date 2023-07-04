from django.urls import path
from . import views
urlpatterns = [
    # path('<int:pk>/', views.NoteDetail.as_view()),
    path('', views.Entries.as_view()),
    path('category', views.Category.as_view()),
    path('search', views.Search.as_view())
]