from django.contrib import admin

# Register your models here.
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ("__str__", "updated", "timestamp")
    list_filter = ("title", "updated", "timestamp")
    search_fields = ("title", "updated", "timestamp")
    class Meta:
        model = Post


admin.site.register(Post, PostAdmin)
