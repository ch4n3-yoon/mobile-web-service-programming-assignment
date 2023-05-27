from django import forms
from blog.models import Post as PostModel


class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ('title', 'text',)
