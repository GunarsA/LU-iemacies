from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path("", views.SubjectListView.as_view(), name="home"),

    path("subject/", views.SubjectListView.as_view(), name="subjects"),
    path("subject/<int:pk>", views.SubjectDetailView.as_view(), name="subject_detail"),

    path("advert/", views.AdvertListView.as_view(), name="adverts"),
    path("advert/<int:pk>", views.AdvertDetailView.as_view(), name="advert_detail"),
    path("advert/create", views.AdvertCreateView.as_view(), name="advert_create"),
    path("advert/create/<int:pk>", views.AdvertCreateView.as_view(), name="advert_create"),
    path("advert/<int:pk>/update", views.AdvertUpdateView.as_view(), name="advert_update"),

    path("application/create/<int:pk>", views.createApplication, name="application_create"),
    path("application/<int:pk>", views.viewApplication, name="application_detail"),

    path("chat/", views.chatListView, name="chats"),
    path("chat/<int:pk>", views.chatDetailView, name="chat_detail"),

    path("profile/<int:pk>", views.profileDetailView, name="profile_detail"),
    path("profile/<int:pk>/update", views.profileUpdateView, name="profile_update"),

    path("review/create/<int:pk>", views.createReview, name="review_create"),
    path("review/<int:pk>", views.viewReview, name="review_detail"),
    path("review/<int:pk>/update", views.updateReview, name="review_update"),
]
