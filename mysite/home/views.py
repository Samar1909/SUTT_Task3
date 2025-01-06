from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import *
from .forms import *    
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.views.generic import (DetailView, UpdateView, ListView, CreateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import timedelta
from django.core.paginator import Paginator
# Create your views here.

def home_page(request):
    current = request.user
    if current.is_authenticated:
        email = current.email
        if "@pilani.bits-pilani.ac.in" in email:
            current.save()
            current.profile.is_student = True
            current.profile.save()
            return redirect('student-home')
        
        elif request.user.profile.is_librarian == True:
            messages.success(request, f'Successfully Signed-In as {current.username}')
            return redirect('librarian-home')
        
        else:
            for message in messages.get_messages(request):
                pass
            messages.error(request, f'Pls enter a valid BITS email')
            current.delete()
            return redirect('home-page')
    else:
        return render(request, 'home/base.html')


#librarian views start here
@login_required
def librarian_home(request):
    return render(request, "home/lib_home.html")

@login_required
def librarian_addBookForm(request):
    return render(request, 'home/lib_addBookForm.html')

@login_required
def addBook(request):
    if request.method == 'POST':
        book = books.objects.create(
        name = request.POST['name'],
        author = request.POST['author'],
        pub = request.POST['pub'],
        isbn = request.POST['ISBN'],
        copies_total = request.POST['copies_total'],
        copies_available = request.POST['copies_total']
        )
        book.save()
        messages.success(request, f'{book.name} added to Library!') 
        return redirect("librarian-home")
    else:
        return HttpResponse("404 - Not allowed")
    
@login_required
def addBookExcel(request):
    if request.method == "POST":
        file = request.FILES['files']
        try:
            df = pd.read_excel(file)    
            for i in range(0, len(df)):
                books.objects.create(
                    name = df['Name'][i],
                    author = df['Author'][i],
                    pub = df['Publisher Name'][i],
                    isbn = df['ISBN Code'][i],
                    copies_total = df['Number of copies available'][i],
                    copies_available = df['Number of copies available'][i],  
                )
            messages.success(request, f'{len(df)} books added to Library!')
            return redirect('librarian-home')
        except Exception as e:
            messages.error(request, f'Error: {e}')
            return redirect('librarian-home')
    else:
        return render(request, "home/lib_addBookExcel.html")
    
@login_required
def listOfBooks(request):
    if request.user.profile.is_student == True:
        base_template = 'home/stu_base.html'
    else:
        base_template = 'home/lib_base.html'

    book_list = books.objects.all()
    paginator = Paginator(book_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "books": page_obj,
        "base_template": base_template
    }
    return render(request, 'home/lib_ListofBooks.html', context)


def lib_bookDetailPage(request, pk):
    book = books.objects.filter(id = pk).first()
    rate_set = book.rate_set.all()
    sum = 0; avgRating = 0
    if rate_set.count() != 0:
        for rate in rate_set:
            sum += rate.rating
        avgRating = sum/rate_set.count()
    context = {
        'book' : book,
        'avgRating' : avgRating
    }
                
    return render (request, 'home/lib_bookDetail.html', context)
    

class lib_bookUpdatePage(LoginRequiredMixin, UpdateView):
    model = books
    fields = ['name', 'author', 'pub', 'isbn', 'copies_total', 'copies_available', 'copies_total']
    template_name = 'home/lib_bookUpdate.html'

    def form_valid(self, form):
        return super().form_valid(form)
    
class lib_paramsDetails(LoginRequiredMixin, DetailView):
    model = library_settings
    template_name = 'home/lib_paramsDetail.html'

class lib_paramsUpdate(LoginRequiredMixin, UpdateView):
    model = library_settings
    fields = ['late_fees', 'issue_period']
    template_name = 'home/lib_bookUpdate.html'

@login_required
def lib_borrowList(request, pk):
    book = books.objects.filter(id = pk).first()
    borrowers = book.borrowbook_set.all()
    if not borrowers.exists():
        messages.info(request, f'No one has borrowed {book.name} currently')
        return redirect('lib_book-page', pk = pk)
    return render(request, 'home/lib_borrowList.html', {"book": book, "borrowers": borrowers})

@login_required
def lib_profileUpdate(request):
    if request.method == 'POST':
        u_form = lib_UserUpdateForm(request.POST, instance = request.user)
        p_form = lib_ProfileUpdateForm(request.POST, 
                                       request.FILES, 
                                       instance = request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('librarian-home')
        
    else:
        u_form = lib_UserUpdateForm(instance = request.user)
        p_form = lib_ProfileUpdateForm(instance = request.user.profile)

    context = {
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request, 'home/lib_profileUpdate.html', context)

class lib_feedbackList(LoginRequiredMixin, ListView):
    model = feedback
    context_object_name = 'feedbacks'
    ordering = ['-date_posted']
    template_name = 'home/lib_feedbackList.html'

#librarian views end here

#student views
def student_home(request):
    if request.user.is_authenticated:
        context = {
            'borrowBooks':request.user.borrowbook_set.all()
        }
        return render(request, "home/stu_home.html", context)
    else:
        messages.error(request, f'You need to login first')
        return redirect('home-page') 
   
def stu_profileUpdate(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance = request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('student-home')
        
    else:
        u_form = UserUpdateForm(instance = request.user)
        p_form = ProfileUpdateForm(instance = request.user.profile)

    context = {
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request, 'home/stu_profileUpdate.html', context)

def HandleSearch(request):
    if request.user.is_authenticated:
        query = request.GET['query']
        if request.user.profile.is_student == True:
            base_template = 'home/stu_base.html'
        else:
            base_template = 'home/lib_base.html'
        
        if len(query) > 85:
            allBooks = []
        else:
            allBooksName = books.objects.filter(name__icontains = query)
            allBooksAuthor = books.objects.filter(author__icontains = query)
            allBooksisbn = books.objects.filter(isbn__icontains = query)
            allBookspub = books.objects.filter(pub__icontains = query)
            allBooks = allBooksName.union(allBooksAuthor, allBooksisbn, allBookspub)
        context = {
            "base_template" : base_template,
            "allBooks" : allBooks,
            "query" : query
        }
        if len(allBooks) == 0:
            messages.warning(request, "No search results found. Please refine your query.")
        return render(request, 'home/handleSearch.html', context)
    else:
        messages.error(request, f'You need to login first')
        return redirect('home-page')
    

def stu_bookDetailPage(request, pk):
    if request.user.is_authenticated:
        book = books.objects.filter(id = pk).first()
        rate_set = book.rate_set.all()
        sum = 0; avgRating = 0
        if rate_set.count() != 0:
            for rate in rate_set:
                sum += rate.rating
            avgRating = sum/rate_set.count()
        context = {
            'book' : book,
            'avgRating' : avgRating
        }
                  
        return render (request, 'home/stu_bookDetail.html', context)
    else:
        messages.error(request, f'You need to login first')
        return redirect('home-page')

def stu_borrowBook(request, pk):
    if request.user.is_authenticated:
        if request.user.profile.is_student == True:
            issue_period = library_settings.objects.filter(id = 1).first().issue_period
            current_book = books.objects.filter(id = pk).first()
            borrow_books = request.user.borrowbook_set.all()
            for borrow_book in borrow_books:
                if borrow_book.book == current_book:
                    messages.error(request, f'You can only borrow one copy of this book at a time')
                    return redirect('stu_book-page', pk = pk)
            newBook = request.user.borrowbook_set.create(book = current_book, params = library_settings.objects.filter(id = 1).first())
            newBook.date_return = newBook.date_borrow + timedelta(days = issue_period)
            newBook.save()
            current_book.copies_available -= 1
            current_book.save()
            messages.success(request, f'You have successfully borrowed {current_book.name}!')
            return redirect('stu_book-page', pk = pk)
        else:
            return HttpResponse("404 - Not Allowed")
    else:
        messages.error(request, f'You need to login first')
        return redirect('home-page')

def stu_returnBook(request, pk):
    if request.user.is_authenticated:
        if request.user.profile.is_student == True:
            current_book = books.objects.filter(id = pk).first()
            borrow_books = request.user.borrowbook_set.all()
            for borrow_book in borrow_books:
                if borrow_book.book == current_book:
                    return_book = request.user.returnbook_set.create(book = current_book, date_return = timezone.now(), date_borrow = borrow_book.date_borrow)
                    current_book.copies_available += 1
                    current_book.save()
                    borrow_book.delete()  
                    messages.success(request, f'You have successfully returned {current_book.name}!')
                    if timezone.now() > borrow_book.date_return:
                        return_book.is_latefees = True
                        return_book.save()
                        messages.success(request, f'You have been charged with Late fees of Rs {library_settings.objects.filter(id = 1).first().late_fees}')
                    return redirect('stu_book-page', pk = pk)
            messages.error(request, f'You have not borrowed this book yet.')
            return redirect('stu_book-page', pk = pk)
        else:
            return HttpResponse("404 - Not Allowed")
    else:
        messages.error(request, f'You need to login first')
        return redirect('home-page')

def stu_issuingHistory(request):
    if request.user.is_authenticated:
        context = {
            'borrowBooks': request.user.borrowbook_set.all(),
            'returnedBooks': request.user.returnbook_set.all(),
            'late_fees': library_settings.objects.filter(id = 1).first().late_fees
        }
        return render(request, 'home/stu_issuingHistory.html', context)
    else:
        messages.error(request, f'You need to login first')
        return redirect('home-page')


class stu_feedback(LoginRequiredMixin, CreateView):
    model = feedback
    fields = ['subject', 'content', 'feedbackImage']
    template_name = 'home/stu_feedback.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class stu_feedbackList(LoginRequiredMixin, ListView):
    model = feedback
    template_name = 'home/stu_feedbackList.html'
    ordering = ['-date_posted']
    context_object_name = 'feedbacks'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the default context
        context = super().get_context_data(**kwargs)
        # Add custom context data
        context['feedbacks'] = self.request.user.feedback_set.all()
        return context

def stu_rating(request, pk):
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 0))
        current_book = books.objects.filter(id = pk).first()
        issueBooks = request.user.borrowbook_set.all().union(request.user.returnbook_set.all())
        for issueBook in issueBooks:
            if current_book == issueBook.book:
                rate.objects.create(user = request.user, rating = rating, book = current_book)
                messages.success(request, f'Your rating was successfully recorded')
                return redirect('stu_book-page', pk)
        messages.error(request, f'You have to borrow {current_book.name} in order to rate it')
        return redirect('stu_book-page', pk)
    else:
        return HttpResponse("404 - Not Allowed")
