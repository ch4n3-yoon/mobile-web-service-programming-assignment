from django.shortcuts import render


def post_list(request):
    return render(request, 'blog/post_list.html', {})


def test(request):
    return render(request, 'blog/test.html', {})
