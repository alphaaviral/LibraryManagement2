from django.shortcuts import render, redirect
from .models import Book, request_detail
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import RequestPeriodForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import datetime
from django.core.mail import send_mail
from Library_management import settings

admin_email ='alphaaviral@gmail.com'

class BookListView(ListView):
    model = Book
    template_name = 'books/home.html'
    context_object_name = 'books'
    ordering = ['-date_added']
    # paginate_by = 5
def home(request):
    return render(request, 'books/main-home.html')

def search_venues(request):
    if request.method == 'POST':
        searched = request.POST.get("searched")
        books = Book.objects.filter(title__contains=searched)|Book.objects.filter(author__contains=searched)|Book.objects.filter(genre__contains=searched)|Book.objects.filter(ISBN__contains=searched)|Book.objects.filter(publisher__contains=searched)
        context={
            'searched': searched,
            'books': books,
        }
    return render(request, 'books/search_venues.html', context)

def BookDetailView(request, **kwargs):
    current_book = Book.objects.filter(id=kwargs['pk'])[0]
    current_user = request.user
    requests_by_user = request_detail.objects.filter(requested_by=current_user)
    that_request_by_user = requests_by_user.filter(book_detail = current_book)

    if  that_request_by_user.filter(request_status = 'Approved').exists():
        ref_request = that_request_by_user.filter(request_status='Approved')[0]
        x=1
    elif that_request_by_user.filter(request_status = 'Pending').exists():
        x=0
        ref_request=0
    else:
        x=2
        ref_request = 0
    context={
        'book': current_book,
        'x': x,
        'request': ref_request,
    }

    return render(request, 'books/book_detail.html', context)

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
    requesting_user=current_request.requested_by.email

    if request.method =='POST':
        current_request.request_status = 'Declined'
        current_request.save()
        send_mail(
            'Book Issue Request',
            'Your request has been declined for'+ current_request.book_detail.title,
            settings.EMAIL_HOST_USER,
            [requesting_user],
            fail_silently=False,
        )
        return redirect('request-list')

    if current_user.has_perm('books.change_book'):
        return render(request, 'books/request_decline.html')
    else:
        raise PermissionDenied

@login_required
def RequestApproveView(request, **kwargs):
    current_request = request_detail.objects.filter(id=kwargs['pk'])[0]
    logged_in_user=request.user
    current_user = current_request.requested_by
    current_user_email=current_user.email
    if request.method =='POST':
        current_request.book_detail.available = False
        current_request.request_status='Approved'
        current_request.save()
        current_request.book_detail.save()
        send_mail(
            'Book Issue Request',
            'Your request has been approved for '+ current_request.book_detail.title,
            settings.EMAIL_HOST_USER,
            [current_user_email],
            fail_silently=False,
        )
        return redirect('request-list')

    else:
        if logged_in_user.has_perm('books.change_book'):
            if current_request.book_detail.available==True:
                return render(request, 'books/request_approve.html')
            else:
                return HttpResponse('<h2>This book is not available!</h2>')
        else:
            raise PermissionDenied
@login_required
def BookReturnView(request, **kwargs):
    current_request = request_detail.objects.filter(id=kwargs['pk'])[0]
    current_user = request.user
    current_date = datetime.datetime.now().date()
    delta = (current_date-current_request.return_date)
    fine = delta.days*20
    if request.method =='POST':
        current_request.book_detail.available=True
        current_request.request_status = 'Returned'
        current_request.save()
        current_request.book_detail.save()
        return redirect('approved-request-list')
    else:
        if current_user.has_perm('books.change_book'):
            if current_request.book_detail.available==False:
                context = {
                    'request': current_request,
                    'fine': fine,
                }

                return render(request, 'books/return_book.html', context)
            else:
                return HttpResponse('<h2>This book is already in stock!</h2>')
        else:
            raise PermissionDenied


class ApprovedRequestListView(LoginRequiredMixin, UserPassesTestMixin, ListView):

    model = request_detail
    template_name = 'books/approved_request_list.html'
    context_object_name = 'requests'
    ordering = ['book_detail']

    def test_func(self):
        current_user = self.request.user
        if current_user.has_perm('books.add_book'):
            return True

        return False

class RenewRequestView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = request_detail
    form_class = RequestPeriodForm
    template_name = 'books/renew_request.html'
    context_object_name = 'form'

    def test_func(self):
        current_request = request_detail.objects.filter(id=self.kwargs.get('pk'))[0]
        current_user= self.request.user
        if current_user.has_perm('books.change_book'):
            return False
        else:
            if current_request.book_detail.available==False:
                current_request.request_status='Pending for renewal'
                return True
            else:
                return HttpResponse('<h2>You cannot return a book you do not have!</h2>')
