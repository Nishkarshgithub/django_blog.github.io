from django.db import models
from django.contrib.auth.models import AbstractUser
from .constant import TRUE_VALUE, FALSE_VALUE, NAME_LENGTH, TITLE_LENGTH, CONTENT_LENGTH


class User(AbstractUser) :
    Is_admin = models.BooleanField (default=FALSE_VALUE)
    Is_user = models.BooleanField (default=FALSE_VALUE)


class Author(models.Model) :
    user = models.ForeignKey (User, on_delete=models.CASCADE)
    Id = models.AutoField (primary_key=TRUE_VALUE)
    name = models.CharField (max_length = NAME_LENGTH)
    createTime = models.DateTimeField (auto_now=FALSE_VALUE, auto_now_add=FALSE_VALUE)
    Is_active = models.BooleanField(default=TRUE_VALUE)

    def __str__(self):
        return self.name + '(, Username: ' + self.user.username + ')'


class Blog(models.Model) :
    Id = models.AutoField (primary_key=TRUE_VALUE)
    created_by = models.ForeignKey (Author, on_delete=models.CASCADE)
    created_at = models.DateTimeField (auto_now=FALSE_VALUE, auto_now_add=FALSE_VALUE)
    title = models.CharField (max_length = TITLE_LENGTH)
    content = models.CharField (max_length = CONTENT_LENGTH)
    is_publised = models.BooleanField(default=FALSE_VALUE)
    is_active = models.BooleanField(default=TRUE_VALUE)

    def __str__(self):
        return self.created_by.name + '(, Blog Title: ' + self.title + ')'


class Comments(models.Model) :
    Id = models.AutoField (primary_key=TRUE_VALUE)
    created_by = models.ForeignKey (Author, on_delete=models.CASCADE)
    created_for = models.ForeignKey (Blog, on_delete=models.CASCADE)
    created_at = models.DateTimeField (auto_now=FALSE_VALUE, auto_now_add=FALSE_VALUE)
    content = models.CharField (max_length = CONTENT_LENGTH)

    def __str__(self):
        return self.created_by.name + '(, Blog: ' + self.created_for.title + ')'