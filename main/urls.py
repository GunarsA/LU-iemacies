from django.urls import path

from . import views

urlpatterns = [
    path("", views.SubjectListView.as_view(), name="index"),
    path("subject/", views.SubjectListView.as_view(), name="subjects"),
    path("subject/<int:pk>", views.SubjectDetailView.as_view(), name="subject_detail"),
    path("advert/", views.AdvertListView.as_view(), name="adverts"),
    path("advert/<int:pk>", views.AdvertDetailView.as_view(), name="advert_detail"),
    path("advert/create", views.AdvertCreateView.as_view(), name="advert_create"),
    path("advert/<int:pk>/update", views.AdvertUpdateView.as_view(), name="advert_update"),
]