from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import post

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ("user_id", "title", "page_type",
                    "time_created", "time_modified")

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "user_type")

admin.site.register(post, PostAdmin)
admin.site.register(get_user_model(), UserAdmin)
