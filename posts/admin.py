from django.contrib import admin
from .models import post

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ("user_id", "text", "timeCreated", "timeModified")

admin.site.register(post, PostAdmin)
