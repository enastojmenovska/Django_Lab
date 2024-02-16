from django.shortcuts import render, redirect
from .models import Post, Blogger, BloggerBlockedUser
from .forms import PostForm, BloggerBlockedUserForm


# Create your views here.

def posts(request):
    blogger = Blogger.objects.get(user=request.user)
    blocked_bloggers = BloggerBlockedUser.objects.filter(blogger=blogger).values_list("blocked_user", flat=True)
    posts_filtered = Post.objects.exclude(author__user__in=blocked_bloggers).exclude(author=blogger)
    dictionery = {'posts': posts_filtered}
    return render(request, 'index_posts.html', context=dictionery)


def add_post(request):
    if request.method == "POST":
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = Blogger.objects.get(user=request.user)
            post.save()
            return redirect("profile")
    dictionery = {"form": PostForm}
    return render(request, "add_post.html", context=dictionery)


def profile(request):
    posts_filtered = Post.objects.filter(author__user=request.user)
    dictionery = {"posts": posts_filtered, "blogger": Blogger.objects.get(user=request.user)}
    return render(request, "profile.html", context=dictionery)


def blockedUsers(request):
    if request.method == "POST":
        form = BloggerBlockedUserForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            blocked_user = form.save(commit=False)
            blocked_user.blogger = Blogger.objects.get(user=request.user)
            blocked_user.save()
            return redirect("blockedUsers")
    blogger = Blogger.objects.get(user=request.user)
    blocked_by_blogger_users = BloggerBlockedUser.objects.filter(blogger=blogger).values_list("blocked_user", flat=True)
    blocked_by_blogger = []
    for b in blocked_by_blogger_users:
        blocked_blogger = Blogger.objects.get(user=b)
        blocked_by_blogger.append(blocked_blogger)
    dictionery = {"blogger": blogger, "blocked_bloggers": blocked_by_blogger, "form": BloggerBlockedUserForm}
    return render(request, "blockedUsers.html", context=dictionery)
