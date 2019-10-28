from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):  # add this
    list_display = ('title', 'content', 'date_posted', 'image')  # add this


admin.site.register(Post, PostAdmin)

