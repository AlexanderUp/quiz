from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import UserSignupForm


class UserSignupView(CreateView):
    form_class = UserSignupForm
    success_url = reverse_lazy("questions:index")
    template_name = "users/signup.html"
