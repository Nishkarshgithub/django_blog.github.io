from .models import User, Author, Blog, Comments
from rest_framework.response import Response
from django.contrib.auth import login
from datetime import datetime, date, timedelta, tzinfo
from rest_framework.authtoken.models import Token
from rest_framework import viewsets, status

# Constant Import
from .constant import STATUS, DETAIL, FAILURE, SUCCESS, DATA, TOKEN, USERDATA, BLOGDATA

# Serializers Import
from .serializers import AuthorSerializer, UserSerializer, BlogSerializer, CommentsSerializer

def USER_LOGIN(USER, REQUEST):
    login(REQUEST, USER)
    token, bool_value = Token.objects.get_or_create(user=USER)
    Author_Data = Author.objects.get(user=USER)
    return Response({ STATUS: SUCCESS, DETAIL: "USER LOGGED IN", DATA: { TOKEN : token.key, USERDATA : AuthorSerializer(Author_Data).data }}, status.HTTP_200_OK)


def BLOG_CREATE(REQUEST, USER, TITLE, CONTENT, WILL_PUBLISH):
    Blog.objects.create( created_by = USER, created_at = datetime.now(), title = TITLE, content = CONTENT, is_publised = WILL_PUBLISH)
    return Response({ STATUS: SUCCESS, DETAIL: "BLOG CREATED SUCCESSFULLY!" }, status.HTTP_200_OK)
