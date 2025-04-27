from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')