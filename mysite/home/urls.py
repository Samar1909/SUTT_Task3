from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import (lib_bookUpdatePage, lib_paramsDetails, lib_paramsUpdate, stu_feedback, stu_feedbackList, lib_feedbackList, addBookExcel, lib_profileUpdate, favourite_list)
from django.conf import settings
from django.conf.urls.static import static

 
urlpatterns = [
    path('', views.home_page, name = "home-page"),
    path('login/librarian', auth_views.LoginView.as_view(template_name = "home/librarianLogin.html"), name = "LibrarianLogin"),
    path('librarian/home', views.librarian_home, name = "librarian-home"),
    path('logout', auth_views.LogoutView.as_view(template_name = "home/logout.html"), name = "logout"),
    path('librarian/addBookForm', views.librarian_addBookForm, name = "addBookForm"),
    path('librarian/addBook', views.addBook, name = "addBook"),
    path('librarian/addBookExcel', addBookExcel.as_view(), name = "addBookExcel"),
    path('librarian/listOfBooks', views.listOfBooks, name = "lib_listOfBooks"),
    path('librarian/<int:pk>', views.lib_bookDetailPage, name = "lib_book-page"),
    path('librarian/update/<int:pk>', lib_bookUpdatePage.as_view(), name = "lib_book-updatePage"),
    path('librarian/params/<int:pk>', lib_paramsDetails.as_view(), name = "lib_paramsDetail"),
    path('librarian/params/<int:pk>/update', lib_paramsUpdate.as_view(), name = "lib_paramsUpdate"),
    path('librarian/<int:pk>/borrowList', views.lib_borrowList, name = "lib_borrowList"),
    path('librarian/profileUpdate', lib_profileUpdate.as_view(), name = "lib_profileUpdate"),
    path('librarian/feedbackList', lib_feedbackList.as_view(), name = "lib_feedbackList"),
    path('search/', views.HandleSearch, name = "search"),
    path('student/home', views.student_home, name = "student-home"),
    path('student/<int:pk>', views.stu_bookDetailPage, name = "stu_book-page"),
    path('student/borrow/<int:pk>', views.stu_borrowBook, name = "stu_borrowBook"),
    path('student/return/<int:pk>', views.stu_returnBook, name = "stu_returnBook"),
    path('student/issuingHistory', views.stu_issuingHistory, name = "stu_issuingHistory"),
    path('student/feedbackForm', stu_feedback.as_view(), name = "stu_feedback"),
    path('student/<int:pk>/rate', views.stu_rating, name = "stu_rating"),
    path('student/profileUpdate', views.stu_profileUpdate, name = "stu_profileUpdate"),
    path('student/feedbackList', stu_feedbackList.as_view(), name = "stu_feedbackList"),
    path('student/<int:pk>/markFavourite', views.mark_favourite, name = "mark_favourite"),
    path('student/<int:pk>/removeFavourite', views.remove_favourite, name = "remove_favourite"),
    path('student/favouriteList', favourite_list.as_view(), name = "favourite_list")
]  

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
