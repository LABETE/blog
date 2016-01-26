from django import forms
from django.utils.text import slugify

from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("title", "content", "image", "draft", "publish")

    def clean_title(self):
        title = self.cleaned_data["title"]
        slug = slugify(title)
        try:
            Post.objects.get(slug=slug)
            error_msg = forms.ValidationError("This title already exist.")
            self.add_error('title', error_msg)
        except:
            return title
