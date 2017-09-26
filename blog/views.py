import markdown
from django.shortcuts import render, get_object_or_404

from comments.forms import CommentForm
from .models import Post,Category


# Create your views here.
def index(request):
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={
        'post_list': post_list
    })


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    post.increase_views()

    # 记得在顶部引入 markdown 模块
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    form = CommentForm()
    comment_list = post.comment_set.all()
    return render(request, 'blog/detail.html', context={'post': post,
                                                        'form': form,
                                                        'comment_list': comment_list})


def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year, created_time__month=month)
    return render(request, 'blog/index.html', context={'post_list': post_list})


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})
