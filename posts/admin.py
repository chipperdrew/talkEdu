from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import post
#from votes.models import vote

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "title", "page_type",
                    "time_created", "spam_count")

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "user_type", "date_joined")

#class VoteAdmin(admin.ModelAdmin):
#    list_display = ("post_id", "user_id", "vote_choice")

admin.site.register(post, PostAdmin)
admin.site.register(get_user_model(), UserAdmin)
#admin.site.register(vote, VoteAdmin)
