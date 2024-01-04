from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic

from main.forms import UserForm, ProfileForm, AdvertForm, ApplicationForm, ReviewForm
from main.models import Profile, Chat, Advert, Application, Review, Subject


# ---------------------------- Authentication Views ---------------------------


def userLogin(request: HttpRequest) -> HttpResponse:
    """
    View function for the login page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.

    """
    if request.user.is_authenticated:
        return redirect('home')

    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            login(request, user)

            messages.success(request, 'Logged in as ' + user.username)

            return redirect('home')
        else:
            messages.error(request, form.error_messages)

    return render(request, 'main/user_login.html', {'form': form})


def userRegister(request: HttpRequest) -> HttpResponse:
    """
    View function for user registration.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.

    """
    if request.user.is_authenticated:
        return redirect('home')

    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            user.profile = Profile.objects.create(user=user)

            login(request, user)

            messages.success(request, 'User account was created')

            return redirect('home')
        else:
            messages.error(request, form.error_messages)

    return render(request, 'main/user_register.html', {'form': form})


def userLogout(request: HttpRequest) -> HttpResponse:
    """
    Logs out the user and redirects to the home page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: A redirect response to the home page.
    """
    logout(request)

    messages.success(request, 'Logged out successfully')

    return redirect('home')


# ------------------------------ Profile Views --------------------------------


def profileDetail(request: HttpRequest, pk: int) -> HttpResponse:
    """
    View function that displays the profile detail for a given user.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the user.

    Returns:
        HttpResponse: The HTTP response object containing the rendered template.

    Raises:
        Http404: If the user with the given primary key does not exist.
    """
    if not User.objects.filter(id=pk).exists():
        raise Http404("This page does not exist :(")

    profile = User.objects.get(id=pk).profile

    return render(request, 'main/profile_detail.html', {'profile': profile})


@login_required(login_url='login')
def profileUpdate(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Update the profile of a user.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the user.

    Returns:
        HttpResponse: The HTTP response object.

    Raises:
        Http404: If the user with the given primary key does not exist.
    """
    if not User.objects.filter(id=pk).exists():
        raise Http404("This page does not exist :(")

    if request.user != User.objects.get(id=pk):
        messages.error(request, 'You don\'t have edit access to this profile!')
        return redirect(reverse('profile_detail', args=[pk]))

    profile = User.objects.get(id=pk).profile

    user_form = UserForm(instance=profile.user)
    profile_form = ProfileForm(instance=profile)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=profile.user)
        profile_form = ProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, 'Profile was updated successfully!')

            return redirect(reverse('profile_detail', args=[pk]))
        else:
            messages.error(request, user_form.errors.as_text())
            messages.error(request, profile_form.errors.as_text())

    return render(request, 'main/profile_form.html', {'user_form': user_form, 'profile_form': profile_form})


# ------------------------------ Chat Views -----------------------------------


@login_required(login_url='login')
def chatList(request: HttpRequest) -> HttpResponse:
    """
    View function that displays the list of chats for the logged-in user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered chat list template with the chats context.
    """
    chats = request.user.profile.reachable_users()

    return render(request, 'main/chat_list.html', {'chats': chats})


@login_required(login_url='login')
def chatDetail(request: HttpRequest, pk: int) -> HttpResponse:
    """
    View function for displaying the chat detail page.

    Parameters:
    - request: The HTTP request object.
    - pk: The primary key of the user to chat with.

    Returns:
    - If the user or chat does not exist, it redirects to the home page.
    - If the user does not have access to the chat, it redirects to the home page.
    - If the request method is POST and the message is not empty, it creates a new chat message and redirects to the chat detail page.
    - If the request method is POST and the message is empty, it displays a warning message.
    - Otherwise, it renders the chat detail page with the chat messages and receiver information.
    """
    if not User.objects.filter(id=pk).exists():
        messages.error(request, 'This user does not exist!')
        return redirect('home')

    if not request.user.profile.reachable_users().filter(id=pk).exists():
        messages.error(request, 'You don\'t have access to this chat!')
        return redirect('home')

    chat = Chat.objects.filter(sender=request.user, receiver=pk) | Chat.objects.filter(
        sender=pk, receiver=request.user)
    receiver = User.objects.get(id=pk)

    if request.method == 'POST':
        if not request.user.profile.reachable_users().filter(id=pk).exists():
            messages.error(
                request, 'You can no longer send messages to this user!')
            return redirect(reverse('chat_detail', args=[pk]))

        message = request.POST.get('message')
        if message:
            chat = Chat.objects.create(
                sender=request.user, receiver=User.objects.get(id=pk), message=message)
            return redirect(reverse('chat_detail', args=[pk]))
        else:
            messages.warning(request, 'Message cannot be empty!')

    return render(request, 'main/chat_detail.html', {'chat': chat, 'receiver': receiver})


# ------------------------------ Advert Views ---------------------------------


def advertList(request):
    """
    Renders the advert list page.

    Args:
        request: The HTTP request object.

    Returns:
        The rendered advert list page.
    """
    return render(request, 'main/advert_list.html', {'advert_list': Advert.objects.filter(is_active=True)})


@login_required(login_url='login')
def advertCreate(request: HttpRequest, pk: int = None) -> HttpResponse:
    """
    Create a new advertisement.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int, optional): The primary key of the subject related to the advertisement. Defaults to None.

    Returns:
        HttpResponse: The HTTP response object.

    """
    template_name = 'main/advert_form.html'
    success_url = reverse('home')

    initial_data = {}
    if pk:
        initial_data['subject'] = pk

    if Advert.objects.filter(subject=pk, owner=request.user).exists():
        messages.warning(
            request, 'You have already created an advert for this subject!')
        return redirect(reverse('advert_update', args=[Advert.objects.get(subject=pk, owner=request.user).id]))

    if request.method == 'POST':
        form = AdvertForm(request.POST)
        if form.is_valid():
            advert = form.save(commit=False)
            advert.owner = request.user
            advert.save()
            return redirect(success_url)
        else:
            messages.error(request, form.errors.as_text())
    else:
        form = AdvertForm(initial=initial_data)

    return render(request, template_name, {'form': form, 'page': 'create'})


def advertDetail(request: HttpRequest, pk: int) -> HttpResponse:
    """
    View function to display the details of an advert.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the advert.

    Returns:
        HttpResponse: The HTTP response object containing the rendered template.
    """
    template_name = 'main/advert_detail.html'

    advert = get_object_or_404(Advert, pk=pk)

    return render(request, template_name, {'advert': advert})


@login_required(login_url='login')
def advertUpdate(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Update an existing advert.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the advert to be updated.

    Returns:
        HttpResponse: The HTTP response object.

    Raises:
        Http404: If the advert with the given primary key does not exist.
    """
    template_name = 'main/advert_form.html'
    success_url = reverse('home')

    advert = get_object_or_404(Advert, pk=pk)

    if request.user != advert.owner:
        messages.error(request, 'You don\'t have edit access to this advert!')
        return redirect(reverse('advert_detail', args=[pk]))

    if request.method == 'POST':
        form = AdvertForm(request.POST, instance=advert)
        if form.is_valid():
            form.save()
            return redirect(success_url)
        else:
            messages.error(request, form.errors.as_text())
    else:
        form = AdvertForm(instance=advert)

    return render(request, template_name, {'form': form, 'page': 'update'})


# ------------------------------ Application Views ----------------------------


@login_required(login_url='login')
def createApplication(request: HttpRequest, pk: int) -> HttpResponse:
    template_name = 'main/application_form.html'

    if Application.objects.filter(advert=pk, applicant=request.user).exists():
        messages.error(request, 'You have already applied for this advert')
        return redirect(reverse('application_update', args=[Application.objects.get(advert=pk, applicant=request.user).id]))

    advert = get_object_or_404(Advert, pk=pk)

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.advert = advert
            application.applicant = request.user
            application.save()
            return redirect('home')
        else:
            messages.error(request, form.errors.as_text())
    else:
        form = ApplicationForm()

    context = {'form': form, 'advert_name': advert, 'page': 'create'}
    return render(request, template_name, context)


@login_required(login_url='login')
def viewApplication(request: HttpRequest, pk: int) -> HttpResponse:
    template_name = 'main/application_detail.html'

    application = get_object_or_404(Application, pk=pk)

    if (request.user != Application.objects.get(id=pk).advert.owner
            and request.user != Application.objects.get(id=pk).applicant):
        messages.error(request, 'You don\'t have access to this application!')
        return redirect('home')

    if request.method == 'POST':
        application.status = request.POST.get('status').upper()
        application.save()
        return redirect(reverse('application_detail', args=[pk]))

    return render(request, template_name, {'application': application})


@login_required(login_url='login')
def updateApplication(request: HttpRequest, pk: int) -> HttpResponse:
    template_name = 'main/application_form.html'

    application = get_object_or_404(Application, pk=pk)

    if request.user != Application.objects.get(id=pk).applicant:
        messages.error(
            request, 'You don\'t have edit access to this application!')
        return redirect('home')

    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            return redirect(reverse('application_detail', args=[pk]))
        else:
            messages.error(request, form.errors.as_text())
    else:
        form = ApplicationForm(instance=application)

    context = {'form': form, 'advert_name': application.advert, 'page': 'update'}
    return render(request, template_name, context)


# ------------------------------ Review Views --------------------------------


@login_required(login_url='login')
def createReview(request: HttpRequest, pk: int) -> HttpResponse:
    template_name = 'main/review_form.html'

    advert = get_object_or_404(Advert, pk=pk)

    if Review.objects.filter(advert=pk, reviewer=request.user).exists():
        messages.error(request, 'You have already reviewed this advert')
        return redirect(reverse('review_detail', args=[Review.objects.get(advert=pk, reviewer=request.user).id]))

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.advert = advert
            review.reviewer = request.user
            review.save()
            return redirect(reverse('advert_detail', args=[pk]))
        else:
            messages.error(request, form.errors.as_text())
    else:
        form = ReviewForm()

    context = {'form': form, 'advert_name': advert, 'page': 'create'}
    return render(request, template_name, context)


def viewReview(request: HttpRequest, pk: int) -> HttpResponse:
    template_name = 'main/review_detail.html'

    review = get_object_or_404(Review, pk=pk)

    return render(request, template_name, {'review': review})


@login_required(login_url='login')
def updateReview(request: HttpRequest, pk: int) -> HttpResponse:
    template_name = 'main/review_form.html'

    review = get_object_or_404(Review, pk=pk)

    if request.user != Review.objects.get(id=pk).reviewer:
        messages.error(request, 'You don\'t have edit access to this review!')
        return redirect(reverse('review_detail', args=[pk]))

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect(reverse('review_detail', args=[pk]))
        else:
            messages.error(request, form.errors.as_text())
    else:
        form = ReviewForm(instance=review)

    context = {'form': form, 'advert_name': review.advert, 'page': 'update'}
    return render(request, template_name, context)


# ------------------------------ Subject Views -------------------------------

def subjectList(request: HttpRequest) -> HttpResponse:
    template_name = 'main/subject_list.html'

    subjects = Subject.objects.all()
    
    return render(request, template_name, {'subject_list': subjects})


def subjectDetail(request: HttpRequest, pk: int) -> HttpResponse:
    template_name = 'main/subject_detail.html'

    subject = get_object_or_404(Subject, pk=pk)
    
    return render(request, template_name, {'subject': subject})
