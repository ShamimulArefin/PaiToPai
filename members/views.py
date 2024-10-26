from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.urls import reverse
from django.contrib.auth.views import LoginView
from .forms import UserRegistrationForm

def register(request):
    if request.user.is_authenticated:
        return redirect('category_list')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after registration
            return redirect('category_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

class CustomLoginView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('category_list')  # Redirect if already logged in
        return super().dispatch(request, *args, **kwargs)
    
def logout_view(request):
    if request.method == 'GET' or request.method == 'POST':
        logout(request)
        return redirect(reverse('login'))
    
"""
{% if user.is_authenticated %}
    <form action="{% url 'logout' %}" method="post">
        {% csrf_token %}
        <button type="submit">Logout</button>
    </form>
{% endif %}

"""