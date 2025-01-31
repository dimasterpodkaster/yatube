from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
from .models import Post, Group, Follow
# from django.views.generic import CreateView
# from django.urls import reverse_lazy
from .forms import PostForm, CommentForm, FollowForm
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

User = get_user_model()


@cache_page(20, key_prefix='index_page')
def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)  # показывать по 10 записей на странице.

    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    return render(
        request,
        'index.html',
        {'page': page, 'paginator': paginator}
    )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group).order_by("-pub_date").all()
    paginator = Paginator(post_list, 10)  # показывать по 10 записей на странице.

    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    return render(request, "group.html", {"group": group, "page": page, "paginator": paginator})


# class NewPost(CreateView):
#     form_class = PostForm
#     success_url = reverse_lazy("index")
#     template_name = "new_publication.html"


@login_required(login_url='/auth/login/')
def new_post(request):
    method_new = True
    if request.method == 'POST':
        form = PostForm(request.POST, files=request.FILES or None)

        if form.is_valid():
            listing = form.save(commit=False)
            listing.author = request.user
            listing.save()
            return redirect('index')

        return render(request, 'new_publication.html', {'form': form, 'method': method_new})

    form = PostForm()
    return render(request, 'new_publication.html', {'form': form, 'method': method_new})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    subscribed_to = Follow.objects.filter(user=user).count()
    subscribers = Follow.objects.filter(author=user).count()
    if request.user.is_authenticated:
        following_check = Follow.objects.filter(
            user=request.user,
            author=get_object_or_404(User, username=username)).count()
    else:
        following_check = False
    post_list = Post.objects.filter(author=user).order_by("-pub_date").all()
    paginator = Paginator(post_list, 10)  # показывать по 10 записей на странице.

    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    return render(request, 'profile.html', {
        "user_request": user,
        "page": page,
        "paginator": paginator,
        "following": following_check,
        "subscribed_to": subscribed_to,
        "subscribers": subscribers
    })


@login_required(login_url='/auth/login/')
def post_view(request, username, post_id):
    user = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=user, pk=post_id).order_by("-pub_date").all()
    count = Post.objects.filter(author=user).count()
    form = CommentForm()
    items = get_object_or_404(Post, author=user, pk=post_id).comments.all()
    return render(request, 'post.html', {"user_request": user, "posts": post_list, "count": count,
                                         "form": form, "items": items})


@login_required(login_url='/auth/login/')
def post_edit(request, username, post_id):
    method_new = False
    user_request = get_object_or_404(User, username=username)
    selected_post = get_object_or_404(Post, pk=post_id, author=user_request.id)

    if user_request != request.user:
        return redirect('post_view', username=username, post_id=post_id)

    form = PostForm(request.POST or None, files=request.FILES or None, instance=selected_post)
    if request.method == 'POST':
        if form.is_valid():
            selected_post.save()
            return redirect('post', username=username, post_id=post_id)

    return render(request, 'new_publication.html', {
        'form': PostForm(instance=selected_post),
        'method': method_new,
        'username': username,
        'post_id': post_id,
        'selected_post': selected_post
    })


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)


@login_required(login_url='/auth/login/')
def add_comment(request, username, post_id):
    if request.method == 'POST':
        form = CommentForm(request.POST, files=request.FILES or None)

        if form.is_valid():
            listing = form.save(commit=False)
            listing.author = request.user
            listing.post = get_object_or_404(Post, pk=post_id)
            listing.save()
            return redirect('post', username=username, post_id=post_id)

        return render(request, 'comments.html', {'form': form, 'username': username, 'post_id': post_id})

    form = CommentForm()
    return render(request, 'comments.html', {'form': form, 'username': username, 'post_id': post_id})


@login_required(login_url='/auth/login/')
def profile_follow(request, username):
    user_follower = get_object_or_404(User, username=request.user.username)
    user_following = get_object_or_404(User, username=username)
    form = FollowForm()
    listing = form.save(commit=False)
    listing.user = user_follower
    listing.author = user_following
    listing.save()
    return redirect('profile', username=username)


@login_required(login_url='/auth/login/')
def profile_unfollow(request, username):
    user_follower = get_object_or_404(User, username=request.user.username)
    user_following = get_object_or_404(User, username=username)
    selected_relations = get_object_or_404(Follow, user=user_follower, author=user_following)
    selected_relations.delete()
    return redirect('profile', username=username)


@login_required(login_url='/auth/login/')
def follow_index(request):
    post_list = Post.objects.filter(author__following__user=request.user).order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)  # показывать по 10 записей на странице.

    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    return render(
        request,
        'follow.html',
        {'page': page, 'paginator': paginator}
    )
