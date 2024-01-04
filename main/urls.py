from django.urls import path

from . import views

urlpatterns = [
    path("", views.SubjectListView.as_view(), name="home"),

    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path("profile/<int:pk>", views.profileDetailView, name="profile_detail"),
    path("profile/<int:pk>/update", views.profileUpdateView, name="profile_update"),

    path("chat/", views.chatListView, name="chat_list"),
    path("chat/<int:pk>", views.chatDetailView, name="chat_detail"),

    path("advert/", views.AdvertListView.as_view(), name="advert_list"),
    path("advert/<int:pk>", views.AdvertDetailView.as_view(), name="advert_detail"),
    path("advert/create", views.AdvertCreateView.as_view(), name="advert_create"),
    path("advert/create/<int:pk>",
         views.AdvertCreateView.as_view(), name="advert_create"),
    path("advert/<int:pk>/update",
         views.AdvertUpdateView.as_view(), name="advert_update"),

    path("application/create/<int:pk>",
         views.createApplication, name="application_create"),
    path("application/<int:pk>", views.viewApplication, name="application_detail"),
     path("application/<int:pk>/update",
           views.updateApplication, name="application_update"),

    path("review/create/<int:pk>", views.createReview, name="review_create"),
    path("review/<int:pk>", views.viewReview, name="review_detail"),
    path("review/<int:pk>/update", views.updateReview, name="review_update"),

    path("subject/", views.SubjectListView.as_view(), name="subject_list"),
    path("subject/<int:pk>", views.SubjectDetailView.as_view(),
         name="subject_detail"),
]
