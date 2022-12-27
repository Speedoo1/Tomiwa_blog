import random
import socket
import time
from datetime import date

import requests
from chardet import detect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from base.ck import addck
from base.models import blog_post, post_comments, sub_comments, blog_like, affiliate, carousel, User
from langdetect import detect


# def favourite_skill(request):


def base(request):
    today = date.today()
    page = random.randint(1, 500)
    next = request.POST.get('next')
    search = str(request.POST.get('search'))

    if next:

        udemiurl = next
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Authorization": "Basic "
                             "S1Y5V1p5VHJ6U2t4S2I5MmpEaUpIWDRVSTlHMVJqT3FOUFlpbUJ6Ujpqc09nRW9lT2tQUzAxcUg2NnhINzkySlNNa3JOSHo3eEk3cVJrNkdBWEQyaFBXMkhONVFTeHU5eG1oMUxtTGVMT1BjVVRqRXRPaW5kNUsyTmVLRE1QVzVKNTRNSkNLc1BGYUV6TURycjhYWThjVER5WGF5Mno1b1B6V0dEOWhlcg==",
            "Content-Type": "application/json;charset=utf-8"
        }
        udemyapi = requests.request('GET', udemiurl, headers=headers, ).json()
        print(udemyapi['count'])
    else:
        udemiurl = 'https://www.udemy.com//api-2.0/courses/?search=' + search.replace(' ',
                                                                                      "%20") + '&price=price-paid&page_size' \
                                                                                               '=21&is_affiliate_agreed=True&language=en'
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Authorization": "Basic "
                             "S1Y5V1p5VHJ6U2t4S2I5MmpEaUpIWDRVSTlHMVJqT3FOUFlpbUJ6Ujpqc09nRW9lT2tQUzAxcUg2NnhINzkySlNNa3JOSHo3eEk3cVJrNkdBWEQyaFBXMkhONVFTeHU5eG1oMUxtTGVMT1BjVVRqRXRPaW5kNUsyTmVLRE1QVzVKNTRNSkNLc1BGYUV6TURycjhYWThjVER5WGF5Mno1b1B6V0dEOWhlcg==",
            "Content-Type": "application/json;charset=utf-8"
        }
        udemyapi = requests.request('GET', udemiurl, headers=headers, ).json()
        print(udemyapi['count'])
        # this are news api for getting latest news from the internet
    url = 'https://newsapi.org/v2/top-headlines?country=ng&apiKey=4698b5f489f140de81a1b5af83d77359'
    post = blog_post.objects.all().order_by('?')
    data = requests.get(url).json()
    caro = carousel.objects.all()
    #

    context = {'post': post, 'news': data['articles'], 'udemy': udemyapi["results"], 'next': udemyapi['next'],
               'previous': udemyapi['previous']}

    return render(request, 'base/index2.html', context)


def add_blog(request):
    cke = addck()
    context = {'cke': cke}
    return render(request, 'base/addblog.html', context)


def singleblog(request, pk):
    # Python Program to Get IP Address

    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)

    print("Your Computer Name is:" + hostname)
    print("Your Computer IP Address is:" + IPAddr)

    post = blog_post.objects.get(id=pk)
    aff = affiliate.objects.all()
    getlike = post.view_set.get_or_create(ip=IPAddr)

    try:
        url = "https://zenquotes.io/api/random"
        moltivate = requests.get(url).json()[0]['q']
    except:
        moltivate = 'Never give up on what you are doing'

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
               'totallike': totallike, 'like': getlike, 'moltivate': moltivate, 'affiliate': aff}
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
    like = post.blog_like_set.filter(username=request.user)
    if like:
        getlike = post.blog_like_set.get(username=request.user)
        getlike.delete()
    else:
        getlike = post.blog_like_set.get_or_create(username=request.user)

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
        pas = request.POST.get('pass')
        rpass = request.POST.get('rpass')
        mail = request.POST.get('email')
        sex = request.POST.get('gender')
        number = request.POST.get('phone')
        address = request.POST.get('address')
        try:
            mail = User.objects.get(email=mail)
        except:
            if pas == rpass:
                get_pass = make_password(pas)
                account = User(username=username, password=get_pass, gender=sex, email=mail, phone=number,
                               address=address)
                if account:
                    account.save()
                    messages.success(request, 'Account Created successfully')
                    return redirect('base:loging')
            else:
                messages.error(request, 'Password Did not match')
                return redirect('base:signup')
        messages.error(request, 'User Already have an Account')

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


def about(request):
    about = User.objects.get(email='azeezadedeji638@gmail.com')
    context = {'about': about}
    return render(request, 'base/about.html', context)


def contact(request):
    return render(request, 'base/contactpage.html')
