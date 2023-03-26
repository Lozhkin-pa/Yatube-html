from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from .models import Post, Group, Follow
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required

NUMBER_OF_POSTS: int = 10
User = get_user_model()


def index(request):
    post_list = Post.objects.select_related('author', 'group').all()
    paginator = Paginator(post_list, NUMBER_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts_list = group.posts.select_related('group').all()
    paginator = Paginator(posts_list, NUMBER_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'group': group,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.select_related('author').all()
    paginator = Paginator(author.posts.all(), NUMBER_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    following = request.user.is_authenticated and Follow.objects.filter(
        user=request.user,
        author=author
    ).exists()
    context = {
        'author': author,
        'posts': posts,
        'page_obj': page_obj,
        'following': following,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    one_post = get_object_or_404(Post, id=post_id)
    form_comment = CommentForm()
    comments = one_post.comments.all()
    context = {
        'one_post': one_post,
        'post_title': one_post.text,
        'form_comment': form_comment,
        'comments': comments,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    context = {
        'form': form,
    }
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', post.author)
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    context = {
        'form': form,
        'is_edit': True,
    }
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post_id)
    if form.is_valid():
        post.save()
        return redirect('posts:post_detail', post_id=post_id)
    return render(request, 'posts/create_post.html', context)


@login_required
def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    # Выбираем автора (author), смотрим, кто на него подписан (following),
    # из подписок автора берем текущего пользователя (user=request.user)
    posts_list = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(posts_list, NUMBER_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    # Подписаться на автора
    author = get_object_or_404(User, username=username)
    follower = Follow.objects.filter(user=request.user, author=author)
    # Если наш текущий пользователь не автор, на которого хотим подписаться,
    # и пользователь еще не подписан на этого автора:
    if request.user != author and not follower.exists():
        Follow.objects.create(user=request.user, author=author)
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    following = Follow.objects.filter(user_id=request.user, author=author)
    if following.exists():
        following.delete()
    return redirect('posts:profile', username=username)
