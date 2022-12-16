from django.contrib import admin

# Register your models here.
from base.models import *

admin.site.register([like_comment, post_comments, blog_post, blog_like, sub_comments, affiliate])
