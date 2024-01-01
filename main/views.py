from django.forms.models import BaseModelForm
from django.http import HttpResponse

from django.views import generic

from main.models import Profile, Chat, Advert, Application, Lesson, Review, Subject, Material

from main.forms import AdvertForm, ApplicationForm

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'main/login_register.html', context)


def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            user.profile = Profile.objects.create(user=user)

            messages.success(request, 'User account was created')

            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'main/login_register.html', {'form': form})


def logoutUser(request):
    logout(request)
    return redirect('home')


class AdvertListView(generic.ListView):
    model = Advert
    template_name = 'main/advert_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_active=True)


@method_decorator(login_required(login_url='login'), name='dispatch')
class AdvertCreateView(generic.CreateView):
    model = Advert
    template_name = 'main/advert_form.html'
    form_class = AdvertForm
    success_url = '/'

    def get_initial(self):
        initial = super().get_initial()
        if self.kwargs.get('pk'):
            initial['subject'] = self.kwargs.get('pk')
        return initial

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_invalid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class AdvertUpdateView(generic.UpdateView):
    model = Advert
    template_name = 'main/advert_form.html'
    form_class = AdvertForm
    success_url = '/'


class AdvertDetailView(generic.DetailView):
    model = Advert
    template_name = 'main/advert_detail.html'


@login_required(login_url='login')
def createApplication(request, pk):
    if Application.objects.filter(advert=pk, applicant=request.user).exists():
        messages.error(request, 'You have already applied for this advert')
        return redirect('home')

    form = ApplicationForm()

    advert = Advert.objects.get(id=pk)

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.advert = advert
            application.applicant = request.user
            application.save()
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during application')

    return render(request, 'main/application_form.html', {'form': form})


class SubjectListView(generic.ListView):
    model = Subject
    template_name = 'main/subject_list.html'


class SubjectDetailView(generic.DetailView):
    model = Subject
    template_name = 'main/subject_detail.html'
