from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.models import BaseModelForm
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic

from main.forms import AdvertForm, ApplicationForm
from main.models import Profile, Chat, Advert, Application, Review, Subject


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
            return render(request, 'main/login_register.html')

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


def profileDetailView(request, pk):
    if not User.objects.filter(id=pk).exists():
        raise Http404("This page does not exist :(")

    profile = User.objects.get(id=pk).profile

    return render(request, 'main/profile_detail.html', {'profile': profile})


@login_required(login_url='login')
def profileUpdateView(request, pk):
    if not User.objects.filter(id=pk).exists():
        raise Http404("This page does not exist :(")

    if request.user != User.objects.get(id=pk):
        messages.error(request, 'You don\'t have access to this profile!')
        return redirect('home')

    profile = User.objects.get(id=pk).profile

    if request.method == 'POST':
        profile.user.username = request.POST.get('username')
        profile.user.save()
        profile.description = request.POST.get('description')
        profile.save()
        return redirect(reverse('profile_detail', args=[pk]))

    return render(request, 'main/profile_form.html', {'profile': profile})


@login_required(login_url='login')
def chatListView(request):
    chats = request.user.profile.reachable_users()
    print(chats[0])
    return render(request, 'main/chat_list.html', {'chats': chats})


@login_required(login_url='login')
def chatDetailView(request, pk):
    if not request.user.profile.reachable_users().filter(id=pk).exists():
        messages.error(request, 'You don\'t have access to this chat!')
        return redirect('home')

    chat = Chat.objects.filter(sender=request.user, receiver=pk) | Chat.objects.filter(
        sender=pk, receiver=request.user)
    receiver = User.objects.get(id=pk)

    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            chat = Chat.objects.create(
                sender=request.user, receiver=User.objects.get(id=pk), message=message)
            return redirect(reverse('chat_detail', args=[pk]))

    return render(request, 'main/chat_detail.html', {'chat': chat, 'receiver': receiver})


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


@login_required(login_url='login')
def viewApplication(request, pk):
    if not Application.objects.filter(id=pk).exists():
        # return 404
        raise Http404("This page does not exist :(")

    if (request.user != Application.objects.get(id=pk).advert.owner
            and request.user != Application.objects.get(id=pk).applicant):
        messages.error(request, 'You don\'t have access to this application!')
        return redirect('home')

    application = Application.objects.get(id=pk)

    if request.method == 'POST':
        application.status = request.POST.get('status').lower()
        application.save()
        return redirect(reverse('application_detail', args=[pk]))

    return render(request, 'main/application_detail.html', {'application': application})


@login_required(login_url='login')
def createReview(request, pk):
    if not Application.objects.filter(id=pk).exists():
        raise Http404("This page does not exist :(")

    if Review.objects.filter(advert=pk, reviewer=request.user).exists():
        messages.error(request, 'You have already reviewed this advert')
        return redirect(reverse('review_detail', args=[Review.objects.get(advert=pk, reviewer=request.user).id]))

    advert = Advert.objects.get(id=pk)

    if request.method == 'POST':
        Review.objects.create(advert=advert, reviewer=request.user,
                              rating=request.POST.get('rating'), review=request.POST.get('review'))
        return redirect(reverse('advert_detail', args=[pk]))

    return render(request, 'main/review_form.html', {'advert': advert})


def viewReview(request, pk):
    if not Review.objects.filter(id=pk).exists():
        raise Http404("This page does not exist :(")

    review = Review.objects.get(id=pk)

    return render(request, 'main/review_detail.html', {'review': review})


@login_required(login_url='login')
def updateReview(request, pk):
    if not Review.objects.filter(id=pk).exists():
        raise Http404("This page does not exist :(")

    if request.user != Review.objects.get(id=pk).reviewer:
        messages.error(request, 'You don\'t have access to this review!')
        return redirect('home')

    review = Review.objects.get(id=pk)

    if request.method == 'POST':
        review.rating = request.POST.get('rating')
        review.review = request.POST.get('review')
        review.save()
        return redirect(reverse('review_detail', args=[pk]))

    return render(request, 'main/review_form.html', {'review': review})


class SubjectListView(generic.ListView):
    model = Subject
    template_name = 'main/subject_list.html'


class SubjectDetailView(generic.DetailView):
    model = Subject
    template_name = 'main/subject_detail.html'
