from django.contrib.auth import login, authenticate, get_user_model
from django.shortcuts import render, redirect
from .forms import ContactForm, LoginForm, RegisterForm

def home(request):
    # print(request.session.get('first_name', 'Unknown'))
    content = {
        "content": 'Home'
    }
    if request.user.is_authenticated:
        content['premium_content'] = 'YEAAAA'
    return render(request, 'home_page.html', content)

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
            return redirect('/')
        else:
            print('Error')
    return render(request, 'auth/login.html', content)

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
    return render(request, 'auth/register.html', content)