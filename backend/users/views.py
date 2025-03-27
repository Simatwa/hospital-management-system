from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView, View
from users.models import CustomUser
from users.forms import CustomUserCreationForm, CustomUserUpdateForm
from django.http import JsonResponse
from django.http.request import HttpRequest
from users.models import CustomUser
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, login_not_required
from django.utils.decorators import method_decorator

# Create your views here.


class Login(View):

    http_method_names = ["get", "post"]

    @method_decorator(login_not_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request: HttpRequest):
        if request.GET.get("next"):
            # Reject redirects to prevent confusing API
            return JsonResponse({"detail": "You have to login first."}, status=403)
        token = request.GET.get("token")
        return self.login_user(request, token)

    def post(self, request: HttpRequest):
        token = request.POST.get("token")
        return self.login_user(request, token)

    def login_user(self, request: HttpRequest, token: str) -> JsonResponse:
        if token is not None:
            try:
                user = CustomUser.objects.get(token=token)
                login(request, user)
                return JsonResponse({"detail": "User authenticated successfully"})
            except CustomUser.DoesNotExist:
                return JsonResponse({"detail": "Invalid token"}, status=400)
        return JsonResponse({"detail": "Token not provided for login"}, status=400)


class Logout(View):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return JsonResponse({"detail": "You have logout successfully"})


class CreateUser(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "user_creation.html"

    success_url = reverse_lazy("users:success")


class UpdateUser(UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = "user_creation.html"

    success_url = reverse_lazy("users:success")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.pk != self.get_object().pk:
            return JsonResponse(
                {"detail": "You can only update your own details"}, status=403
            )
        return super().dispatch(*args, **kwargs)


class DeleteUser(DeleteView):
    model = CustomUser

    success_url = reverse_lazy("users:success")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.pk != self.get_object().pk:
            return JsonResponse(
                {"detail": "You can only delete your own account"}, status=403
            )
        else:
            self.request.user.delete()
            return JsonResponse({"detail": "Account deleted successfully."})


class Success(TemplateView):
    http_method_names = ["get"]

    def get(self, request):
        return JsonResponse({"detail": "Action succeeded"})
