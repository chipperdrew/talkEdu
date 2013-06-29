from django.contrib import admin
from .models import post, eduuser

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ("user_id", "text", "timeCreated", "timeModified")

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "user_type")

admin.site.register(post, PostAdmin)
admin.site.register(eduuser, UserAdmin)
