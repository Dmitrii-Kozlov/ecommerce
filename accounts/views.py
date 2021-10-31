from django.contrib.auth import login, authenticate, get_user_model
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .forms import LoginForm, RegisterForm, GuestForm
from .models import GuestEmail


def guest_register_view(request):
    form = GuestForm(request.POST or None)
    content = {
        "form": form
    }
    next_ = request.GET.get('next')
    post_next_ = request.POST.get('next')
    redirect_path = next_ or post_next_ or None
    if form.is_valid():
        email = form.cleaned_data.get('email')
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect('/register/')
    else:
        print('Error')
    return redirect('/register/')


def login_page(request):
    form = LoginForm(request.POST or None)
    content = {
        "form": form
    }
    next_ = request.GET.get('next')
    post_next_ = request.POST.get('next')
    redirect_path = next_ or post_next_ or None
    if form.is_valid():
        try:
            del request.session['guest_email_id']
        except:
            pass
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('/')
        else:
            print('Error')
    return render(request, 'accounts/login.html', content)

User = get_user_model()

def register_page(request):
    form = RegisterForm(request.POST or None)
    content = {
        "form": form
    }
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        new_user = User.objects.create_user(username=username, email=email, password=password)
        print(new_user)
        return redirect('/login')
    return render(request, 'accounts/register.html', content)