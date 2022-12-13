from django.forms import ModelForm

from base.models import blog_post


class addck(ModelForm):
    class Meta:
        model = blog_post
        fields = ['topic', 'image', 'body']
