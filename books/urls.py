from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='main-home'),
    path('library/', views.BookListView.as_view(), name='book-list'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('book/new/', views.BookCreateView.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
    path('<int:pk>/request/new/', views.RequestCreateView.as_view(), name='request-create'),
    path('request/list/', views.RequestListView.as_view(), name='request-list'),
    path('request/<int:pk>/decline/', views.RequestDeclineView, name='request-decline'),
    path('request/<int:pk>/approve/', views.RequestApproveView, name='request-approve'),
]