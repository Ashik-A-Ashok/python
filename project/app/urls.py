from django.urls import path
from.import views


urlpatterns = [

    #path('',views.home),


    path('register',views.register),
    path('',views.login),
    path('welcome',views.welcome),
    path('uploadimgs',views.upload_img),
    path('view_comments',views.view_comments,name='view_comments'),
    path('delete<str:pk>',views.delete,name='delete'),
    path('logout',views.logout1),
    path('detect<str:pk>',views.detect,name='detect'),

    # path('profile<str:pk>', views.profile, name='profile'),



]
