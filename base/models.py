import uuid

from PIL import Image
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User, AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    username = models.CharField(max_length=200)
    gender = models.CharField(max_length=50, null=True)

    address = models.CharField(max_length=500, null=True)

    about_me = RichTextUploadingField(blank=True, null=True, )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class blog_post(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    topic = models.CharField(max_length=300, null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    body = RichTextUploadingField(blank=True, null=True, )

    def __str__(self):
        return str(self.topic)

    @property
    def totalcoment(self):
        comment = post_comments.objects.filter(blog=self.body).count()
        return int(comment)


class post_comments(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    blog = models.ForeignKey(blog_post, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.message)


class blog_like(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(blog_post, on_delete=models.CASCADE, null=True, blank=True)
    like = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return str(self.blog)


class like_comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(blog_post, on_delete=models.CASCADE)
    comment = models.ForeignKey(post_comments, on_delete=models.CASCADE)
    like = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return str(self.comment) + '' + str(self.like)


class sub_comments(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(post_comments, on_delete=models.CASCADE, null=True, blank=True)
    blog = models.ForeignKey(blog_post, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.message)


class affiliate(models.Model):
    link = models.TextField(blank=True, null=True)


class favorite_digital_skill(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.TextField()
    price = models.TextField()
    url = models.TextField()
    title = models.TextField()
    headline = models.TextField()


class carousel(models.Model):
    image = models.ImageField()
    quote = models.CharField(max_length=500)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            size = 400, 300
            img.thumbnail(size, Image.LANCZOS)
            img.save(self.image.path)


class view(models.Model):
    blog = models.ForeignKey(blog_post, on_delete=models.CASCADE)
    ip = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.ip)
