from django.urls import path, include
from . import api_logic as LOGIC

urlpatterns = [
    path('login/', LOGIC.Loginview.as_view()),
    path('logout/', LOGIC.UserLogout.as_view()),
    path('blog/create/', LOGIC.BLOG.as_view({'get': 'create'})),
    path('blog/list/', LOGIC.BLOG.as_view({'get': 'list'})),
    path('blog/delete/', LOGIC.BLOG.as_view({'get': 'destroy'})),
    path('blog/comment/', LOGIC.BLOG.as_view({'get': 'comment'})),
]