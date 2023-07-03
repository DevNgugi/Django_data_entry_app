from django.urls import path
from . import views
urlpatterns = [
    # path('', views.NoteList.as_view()),
    # path('<int:pk>/', views.NoteDetail.as_view()),
    path('db', views.getDB),
    path('add', views.add),
    path('search/<slug:category>', views.Search.as_view())
]