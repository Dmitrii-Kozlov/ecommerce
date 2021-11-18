from django.contrib.auth import login, authenticate, get_user_model
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.views.generic import CreateView, FormView

from .forms import LoginForm, RegisterForm, GuestForm
from .models import GuestEmail
from .signals import user_logged_in_signal


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


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/login/'


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = '/'
    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        post_next_ = request.POST.get('next')
        redirect_path = next_ or post_next_ or None
        try:
            del request.session['guest_email_id']
        except:
            pass
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            user_logged_in_signal.send(user.__class__, instance=user, request=request)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('/')
        return super(LoginView, self).form_invalid(form)

#
#
# def login_page(request):
#     form = LoginForm(request.POST or None)
#     content = {
#         "form": form
#     }
#     next_ = request.GET.get('next')
#     post_next_ = request.POST.get('next')
#     redirect_path = next_ or post_next_ or None
#     if form.is_valid():
#         try:
#             del request.session['guest_email_id']
#         except:
#             pass
#         username = form.cleaned_data.get('username')
#         password = form.cleaned_data.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             if is_safe_url(redirect_path, request.get_host()):
#                 return redirect(redirect_path)
#             else:
#                 return redirect('/')
#         else:
#             print('Error')
#     return render(request, 'accounts/login.html', content)

# User = get_user_model()



# def register_page(request):
#     form = RegisterForm(request.POST or None)
#     content = {
#         "form": form
#     }
#     if form.is_valid():
#         form.save()
#         return redirect('/login')
#     return render(request, 'accounts/register.html', content)