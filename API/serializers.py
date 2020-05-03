from rest_framework import serializers
from .models import User, Author, Blog, Comments


class UserSerializer (serializers.ModelSerializer) :
  class Meta :
    model = User
    fields = ( 'id', 'username', 'password', 'is_admin', 'Is_user' )
  

class AuthorSerializer (serializers.ModelSerializer) :
  class Meta :
    model = Author
    fields = ( 'name', 'createTime', 'Is_active' ) 


class BlogSerializer (serializers.ModelSerializer) :
  class Meta :
    model = Blog
    fields = '__all__'


class CommentsSerializer (serializers.ModelSerializer) :
  class Meta :
    model = Comments
    fields = '__all__'
