from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='main-home'),
    path('library/', views.BookListView.as_view(), name='book-list'),
    path('search_venues/', views.search_venues, name='search-venues'),
    path('book/<int:pk>/', views.BookDetailView, name='book-detail'),
    path('book/new/', views.BookCreateView.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
    path('<int:pk>/request/new/', views.RequestCreateView.as_view(), name='request-create'),
    path('request/list/', views.RequestListView.as_view(), name='request-list'),
    path('request/<int:pk>/decline/', views.RequestDeclineView, name='request-decline'),
    path('request/<int:pk>/approve/', views.RequestApproveView, name='request-approve'),
    path('request/<int:pk>/return/', views.BookReturnView, name='book-return'),
    path('approved-request/list/', views.ApprovedRequestListView.as_view(), name='approved-request-list'),
    path('request/<int:pk>/renew/', views.RenewRequestView.as_view(), name='renew-request'),
]