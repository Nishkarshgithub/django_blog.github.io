from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Author, Blog, Comments, User

admin.site.site_header = "TEST BLOG ADMIN INTERFACE"

admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
  add_fieldsets = (
    (None, {'fields': ('username','password1','password2', 'Is_admin', 'Is_user',)}),
  )
  fieldsets = (
    (None, {'fields': ('username', 'password', 'Is_admin', 'Is_user', 'last_login',)}),
  )
  list_display = ('username', 'Is_admin', 'Is_user',)
  search_fields = ('username',)

admin.site.register(User, UserAdmin)

class Author_Admin(admin.ModelAdmin):
	list_display = ('name','Is_active',)
	list_filter = ('createTime',)

admin.site.register(Author, Author_Admin)

class Blog_Admin(admin.ModelAdmin):
	list_display = ('created_by','title','content','is_publised',)
	list_filter = ('created_at',)

admin.site.register(Blog, Blog_Admin)

class Comments_Admin(admin.ModelAdmin):
	list_display = ('created_by','created_for','content',)
	list_filter = ('created_at',)

admin.site.register(Comments, Comments_Admin)
