from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Article
from .models import Comment
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


@login_required
def post_comment(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    # 处理 POST 请求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            new_comment.save()
            return redirect(article)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 处理错误请求
    else:
        return HttpResponse("发表评论仅接受POST请求。")
