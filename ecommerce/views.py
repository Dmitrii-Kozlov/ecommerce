from django.shortcuts import render

def home(request):
    return render(request, 'home_page.html', {"content": 'Home'})

def about(request):
    return render(request, 'home_page.html', {"content": "About"})

def contact(request):
    if request.method == 'POST':
        print(f"Your name is {request.POST.get('fullname')}")
    return render(request, 'contact/view.html', {"content": "Contact"})