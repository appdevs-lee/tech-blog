from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.views import LogoutView as AuthLogoutView
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CustomUserCreationForm, CustomAuthenticationForm

class SignUpView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('post_list')
    success_message = "회원가입이 완료되었습니다."
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('post_list')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class LoginView(SuccessMessageMixin, AuthLoginView):
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'
    success_message = "로그인되었습니다."
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('post_list')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('post_list')

class LogoutView(AuthLogoutView):
    next_page = reverse_lazy('post_list')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('post_list')
        return super().dispatch(request, *args, **kwargs)