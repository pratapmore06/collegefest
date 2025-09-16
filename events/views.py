from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Event, Participation
from django.contrib import messages

def home(request):
    events = Event.objects.all().order_by('date')
    return render(request, 'events/home.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    participated = False
    if request.user.is_authenticated:
        participated = Participation.objects.filter(user=request.user, event=event).exists()
    return render(request, 'events/event_detail.html', {'event': event, 'participated': participated})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'events/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'events/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def participate_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    participation, created = Participation.objects.get_or_create(user=request.user, event=event)
    if created:
        messages.success(request, f"You have successfully registered for {event.title}.")
    else:
        messages.info(request, f"You are already registered for {event.title}.")
    return redirect('event_detail', event_id=event_id)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import ParticipationForm

@login_required
def my_participations(request):
    participations = Participation.objects.filter(user=request.user).select_related('event').order_by('-participated_at')
    return render(request, 'events/my_participations.html', {'participations': participations})

@login_required
def edit_participation(request, pk):
    participation = get_object_or_404(Participation, pk=pk)
    if participation.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this participation.")

    if request.method == 'POST':
        form = ParticipationForm(request.POST, instance=participation)
        if form.is_valid():
            form.save()
            messages.success(request, "Participation updated successfully.")
            return redirect('my_participations')
    else:
        form = ParticipationForm(instance=participation)

    return render(request, 'events/edit_participation.html', {'form': form, 'participation': participation})

@login_required
def delete_participation(request, pk):
    participation = get_object_or_404(Participation, pk=pk)
    if participation.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this participation.")

    if request.method == 'POST':
        participation.delete()
        messages.success(request, "Participation cancelled successfully.")
        return redirect('my_participations')

    return render(request, 'events/delete_participation.html', {'participation': participation})