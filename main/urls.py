from django.urls import path

from . import views

urlpatterns = [
    path("", views.subjectList, name="home"),

    path('login/', views.userLogin, name="login"),
    path('register/', views.userRegister, name="register"),
    path('logout/', views.userLogout, name="logout"),

    path("profile/<int:pk>", views.profileDetail, name="profile_detail"),
    path("profile/<int:pk>/update", views.profileUpdate, name="profile_update"),

    path("chat/", views.chatList, name="chat_list"),
    path("chat/<int:pk>", views.chatDetail, name="chat_detail"),

    path("advert/", views.advertList, name="advert_list"),
    path("advert/create", views.advertCreate, name="advert_create"),
    path("advert/create/<int:pk>",
         views.advertCreate, name="advert_create"),
    path("advert/<int:pk>", views.advertDetail, name="advert_detail"),
    path("advert/<int:pk>/update",
         views.advertUpdate, name="advert_update"),

    path("application/create/<int:pk>",
         views.createApplication, name="application_create"),
    path("application/<int:pk>", views.viewApplication, name="application_detail"),
    path("application/<int:pk>/update",
         views.updateApplication, name="application_update"),

    path("review/create/<int:pk>", views.createReview, name="review_create"),
    path("review/<int:pk>", views.viewReview, name="review_detail"),
    path("review/<int:pk>/update", views.updateReview, name="review_update"),

    path("subject/", views.subjectList, name="subject_list"),
    path("subject/<int:pk>", views.subjectDetail, name="subject_detail"),

    path("map/", views.map, name="map"),
]
