import time
from datetime import date

import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from base.ck import addck
from base.models import blog_post, post_comments, sub_comments, blog_like


def base(request, ):
    today = date.today()
    url = 'https://newsapi.org/v2/top-headlines?country=ng&apiKey=4698b5f489f140de81a1b5af83d77359'
    post = blog_post.objects.all()
    data = requests.get(url).json()
    print(data)

    context = {'post': post, 'news': data['articles']}

    return render(request, 'base/index2.html', context)


def add_blog(request):
    cke = addck()
    context = {'cke': cke}
    return render(request, 'base/addblog.html', context)


def singleblog(request, pk):
    post = blog_post.objects.get(id=pk)
    getlike = 'Dislike'
    try:
        getlikes = post.blog_like_set.get(username=request.user)
    except:
        getlike = 'Like'
        print(getlike)

    showcomments = post.post_comments_set.all()
    switch = "comment"

    totalcomment = showcomments.count()
    totallike = post.blog_like_set.all().count()
    if request.method == "POST":
        message = request.POST.get('message')
        write = post_comments(blog=post, username=request.user, message=message)
        if write:
            write.save()
            return redirect('base:single', post.id)
        # return redirect('base:single', post.id)

    context = {'post': post, 'comment': showcomments, 'totalcomment': totalcomment, 'switch': switch,
               'totallike': totallike, 'like': getlike}
    return render(request, 'base/sp.html', context)


def sub(request, pk):
    comment = post_comments.objects.get(id=pk)

    if request.method == "POST":
        message = request.POST.get('message')
        previous = request.POST.get('previous', '/')
        subs = sub_comments(username=request.user, message=message, comment=comment)
        if subs:
            subs.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def deletecomment(request, pk):
    comment = post_comments.objects.get(id=pk)
    comment.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


# def updatecomment(request, pk):
#     post = blog_post.objects.get(id=pk)
#     showcomments = post.post_comments_set.all()
#     comment = post_comments.objects.get(id=pk)
#     switch = "updatecomment"
#     context = {'post': post, 'switch': switch, 'comment': comment, 'comments': showcomments}
#     return render(request, 'base/sp.html', context)

@login_required(login_url="base:loging")
def likeblog(request, pk):
    post = blog_post.objects.get(id=pk)
    try:
        getlike = post.blog_like_set.get(username=request.user)
    except:
        getlike = post.blog_like_set.create(username=request.user, like="Like")
        return redirect('base:single', post.id)

    getlike = post.blog_like_set.get(username=request.user)
    getlike.delete()
    return redirect('base:single', post.id)


def loging(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        pas = request.POST.get('pass')
        check = authenticate(request, username=username, password=pas)
        if check:
            login(request, check)
            return redirect('base:index')
        else:
            messages.error(request, "username or password is not correct")

    return render(request, 'base/login.html')


def logoutpage(request):
    logout(request)
    return redirect('base:loging')


def addpost(request):
    page = 'add'
    input = addck()
    if request.method == 'POST':
        form = addck(request.POST, request.FILES)
        if form:
            form.save()
            return redirect('base:index')

    context = {'field': input, 'page': page}
    return render(request, 'base/addblog.html', context)


def createaccout(request):
    if request.method == 'POST':
        username = request.POST.get('username')
    return render(request, 'base/signup.html')


def deletepost(request, pk):
    blogg = blog_post.objects.get(id=pk)
    blogg.delete()
    return redirect("base:index")


def updatepost(request, pk):
    page = 'update'
    blogg = blog_post.objects.get(id=pk)
    form = addck(instance=blogg)
    if request.method == 'POST':
        form = addck(request.POST, request.FILES, instance=blogg)
        if form.is_valid:
            form.save()
            return redirect('base:single', blogg.id)
    context = {'field': form, 'page': page, "post": blogg}
    return render(request, 'base/addblog.html', context)
