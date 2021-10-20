from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import ContactForm, LoginForm

def home(request):
    return render(request, 'home_page.html', {"content": 'Home'})

def about(request):
    return render(request, 'home_page.html', {"content": "About"})

def contact(request):
    contact_form = ContactForm(request.POST or None)
    content = {
        "content": "Contact",
        "form": contact_form
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    # if request.method == 'POST':
    #     print(f"Your name is {request.POST.get('fullname')}")
    #     print(f"Your email is {request.POST.get('email')}")
    #     print(f"Your message is {request.POST.get('content')}")
    return render(request, 'contact/view.html', content)

def login_page(request):
    form = LoginForm(request.POST or None)
    content = {
        "form": form
    }
    print("User logged in")
    print(request.user.is_authenticated)
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # content = {
            #     "form": LoginForm()
            # }
            return redirect('/login')
        else:
            print('Error')
    return render(request, 'auth/login.html', content)

def register_page(request):
    form = LoginForm(request.POST or None)
    content = {
        "form": form
    }
    if form.is_valid():
        print(form.cleaned_data)
    return render(request, 'auth/register.html', content)