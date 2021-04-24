from django.shortcuts import render, redirect
from .models import Book, request_detail
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import RequestPeriodForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

class BookListView(ListView):
    model = Book
    template_name = 'books/home.html'
    context_object_name = 'books'
    ordering = ['-date_added']
    # paginate_by = 5
def home(request):
    return render(request, 'books/main-home.html')

class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

class BookCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'ISBN', 'publisher', 'genre', 'location', 'summary', 'available']
    template_name = 'books/book_add_form.html'
    context_object_name = 'form'


    def test_func(self):
        current_user= self.request.user
        if current_user.has_perm('books.add_book'):
            return True
        return False

class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    fields = ['title', 'author', 'ISBN', 'publisher', 'genre', 'location', 'summary', 'available']
    template_name = 'books/book_update_form.html'
    context_object_name = 'form'

    def test_func(self):
        current_user= self.request.user
        if current_user.has_perm('books.change_book'):
            return True
        return False

class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    template_name = 'books/book_delete_confirm.html'
    context_object_name = 'book'
    success_url = '/library/'
    def test_func(self):
        current_user = self.request.user
        if current_user.has_perm('books.change_book'):
            return True
        return False

class RequestCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = request_detail
    form_class = RequestPeriodForm
    template_name = 'books/request_book.html'
    context_object_name = 'form'


    def test_func(self):
        current_user = self.request.user
        if current_user.has_perm('books.add_book'):
            return False
        return True

    def form_valid(self, form):
        current_book = Book.objects.get(id=self.kwargs.get('pk'))
        form.instance.requested_by = self.request.user
        form.instance.book_detail = current_book
        return super().form_valid(form)

class RequestListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = request_detail
    template_name = 'books/requests_list.html'
    context_object_name = 'requests'
    ordering = ['book_detail']

    def test_func(self):
        current_user = self.request.user
        if current_user.has_perm('books.add_book'):
            return True
        return False

@login_required
def RequestDeclineView(request, **kwargs):
    current_request = request_detail.objects.filter(id=kwargs['pk'])[0]
    current_user = request.user

    if request.method =='POST':
        current_request.request_status = 'Declined'
        current_request.save()
        return redirect('request-list')

    if current_user.has_perm('books.change_book'):
        return render(request, 'books/request_decline.html')
    else:
        raise PermissionDenied

@login_required
def RequestApproveView(request, **kwargs):
    current_request = request_detail.objects.filter(id=kwargs['pk'])[0]
    current_user = request.user
    if request.method =='POST':
        current_request.book_detail.available = False
        current_request.request_status='Approved'
        current_request.save()
        current_request.book_detail.save()
        return redirect('request-list')

    else:
        if current_user.has_perm('books.change_book'):
            return render(request, 'books/request_approve.html')
        else:
            raise PermissionDenied
