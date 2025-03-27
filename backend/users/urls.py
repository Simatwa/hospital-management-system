from django.urls import path
from users.views import Login, CreateUser, UpdateUser, DeleteUser, Success, Logout

urlpatterns = [
    path("success", Success.as_view(), name="success"),
    path("login", Login.as_view(), name="login"),
    path("create", CreateUser.as_view(), name="create"),
    path("update/<int:pk>", UpdateUser.as_view(), name="update"),
    path("delete/<int:pk>", DeleteUser.as_view(), name="delete"),
    path("logout", Logout.as_view(), name="logout"),
]

app_name = "users"
