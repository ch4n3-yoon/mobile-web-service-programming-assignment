from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from rest_framework import viewsets

from blog.models import Post as PostModel
from blog.forms import PostForm
from blog.serializers import PostSerializer


class IntruderImage(viewsets.ModelViewSet):
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer


def post_list(request):
    posts = PostModel.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'user': request.user, 'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(PostModel, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method != 'POST':
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})

    if not request.user:
        return HttpResponse('Unauthorized', status=401)

    form = PostForm(request.POST)
    if not form.is_valid():
        return HttpResponse('Invalid form', status=400)

    post = form.save(commit=False)
    post.author = request.user
    post.published_date = timezone.now()
    post.save()

    return redirect('post_detail', pk=post.pk)


def post_edit(request, pk):
    post = get_object_or_404(PostModel, pk=pk)
    if request.method != 'POST':
        form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})

    if not request.user:
        return HttpResponse('Unauthorized', status=401)

    form = PostForm(request.POST, instance=post)

    if not form.is_valid():
        return HttpResponse('Invalid form', status=400)

    post = form.save(commit=False)
    post.author = request.user
    post.published_date = timezone.now()
    post.save()

    return redirect('post_detail', pk=post.pk)


def test(request):
    return render(request, 'blog/test.html', {})
