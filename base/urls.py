from django.urls import path

from Tomiwa_blog import settings
from base import views

from django.conf.urls.static import static

app_name = 'base'
urlpatterns = [
    path('', views.base, name='index'),
    path('new-blog-post', views.add_blog, name='base'),
    path('single/<str:pk>/', views.singleblog, name='single'),
    path('addsubcomment/<str:pk>', views.sub, name='sub_comment'),
    path('deletecoment/<str:pk>', views.deletecomment, name='deletecomment'),
    path('blog_like/<str:pk>', views.likeblog, name='blog_like'),
    path('login', views.loging, name='loging'),
    path('logout', views.logoutpage, name='logout'),
    path('signup', views.createaccout, name="signup"),
    path('add-post', views.addpost, name="addpost"),
    path('delete-post/<str:pk>', views.deletepost, name='delete'),
    path('update-post/<str:pk>', views.updatepost, name='update'),
    path('about', views.about, name='about'),
    path('contact/', views.contact, name='contact')

]
