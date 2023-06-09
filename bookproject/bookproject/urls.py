"""bookproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from books import views
from django.contrib.auth.views import LoginView,LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls') ),
    path('', views.home_view),

    path('adminclick', views.adminclick_view),
    path('studentclick', views.studentclick_view),


    path('adminsignup', views.adminsignup_view),
    path('studentsignup', views.studentsignup_view),
    path('adminlogin', LoginView.as_view(template_name='books/adminlogin.html')),
    path('studentlogin', LoginView.as_view(template_name='books/studentlogin.html')),

    path('logout', LogoutView.as_view(template_name='books/index.html')),
   # path('logout/<int:id>/', LogoutView.as_view(template_name='books/index.html')),
    path('afterlogin', views.afterlogin_view),
    path('search', views.search, name='search'),
    path('addbook', views.addbook_view, name='addbook'),
    path('viewbook', views.viewbook_view, name='viewbook'),
    path('deleteviewbook', views.deleteviewbook, name='deleteviewbook'),
    path('deleteviewbook/<int:id>/', views.deleteviewbook, name='deleteviewbook'),
   # path('issuebook', views.issuebook_view, name='issuebook'),
    path('viewissuedbook', views.viewissuedbook_view, name='viewissuedbook'),
    path('deleteissuedbook/<int:isbn>/', views.deleteissuedbook, name='deleteissuedbook'),
    path('deleteissuedbook', views.deleteissuedbook, name='deleteissuedbook'),
    path('deleteissuedbookbystudent/<int:isbn>/', views.deleteissuedbook_student, name='deleteissuedbookbystudent'),
    path('deleteissuedbookbystudent', views.deleteissuedbook_student, name='deleteissuedbookbystudent'),
    path('viewstudent', views.viewstudent_view, name='viewstudent'),
    path('viewstudent_delete', views. viewstudent_view_delete, name='viewstudent_delete'),
    path('viewstudent_delete/<int:pk>/', views. viewstudent_view_delete, name='viewstudent_delete'),
    path('viewreservebook_view', views.viewreservebook_view, name='viewreservebook_view'),
    path('viewissuedbookbystudent', views.viewissuedbookbystudent, name='viewissuedbookbystudent'),
    path('viewissuedbookbystudent/logout', LogoutView.as_view(template_name='books/index.html')),
    path('detail/', views.detail, name='detail'),
    path('detail/<int:id>/', views.detail, name='detail'),
    path('detail/<int:id>/logout', LogoutView.as_view(template_name='books/index.html')),
    path('detail/<int:id>/afterlogin', views.afterlogin_view2),
    path('detail/<int:id>/viewissuedbookbystudent', views.viewissuedbookbystudent2, name='viewissuedbookbystudent'),
    path('detail/<int:id>/search', views.search2, name='search'),
   # path('detail/<int:id>issuebook', views.issuebook_view, name='issuebook'),
   # path('detail/<int:id>/issuebook', views.issuebook_view2, name='issuebook'),
    path('detail/<int:id>/bookissuedfinish', views.issuebook_finish, name='bookissuedfinish'),
    path('detail/<int:id>/issuebook_confirm', views.issuebook_confirm, name='issuebook_confirm'),
    path('detail/<int:id>/bookhistory', views.bookhistory2, name='bookhistory'),
    path('detail/<int:id>/reserveviewbyuser', views.reserveviewbyuser2, name='reserveviewbyuser'),
    path('aboutus', views.aboutus_view),
    path('add_reservebook', views.add_book, name='add_reservebook'),
    path('reserveviewbyuser', views.reserveviewbyuser, name='reserveviewbyuser'),
    path('reserveviewbyuser/<int:pk>/', views.reserveviewbyuser, name='reserveviewbyuser'),
    path('reservebook_delete/<int:pk>/', views.reservedeleteviewbyuser, name='reservebook_delete'),
    path('bookhistory', views.bookhistory, name='bookhistory'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = views.error_404page
handler500 = views.error_500page