from django.forms.models import BaseModelForm
from django.http import HttpResponse

from django.views import generic

from main.models import Profile, Message, Advert, Application, Review, Subject, Material

from main.forms import AdvertForm


class AdvertListView(generic.ListView):
    model = Advert
    template_name = 'main/advert_list.html'


class AdvertCreateView(generic.CreateView):
    model = Advert
    template_name = 'main/advert_form.html'
    form_class = AdvertForm
    success_url = '/'
    

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_invalid(form)
    

class AdvertUpdateView(generic.UpdateView):
    model = Advert
    template_name = 'main/advert_form.html'
    form_class = AdvertForm
    success_url = '/'


class AdvertDetailView(generic.DetailView):
    model = Advert
    template_name = 'main/advert_detail.html'
    


class SubjectListView(generic.ListView):
    model = Subject
    template_name = 'main/subject_list.html'


class SubjectDetailView(generic.DetailView):
    model = Subject
    template_name = 'main/subject_detail.html'
