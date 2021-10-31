from django.contrib.auth import login, authenticate, get_user_model
from django.shortcuts import render, redirect
from .forms import ContactForm

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
