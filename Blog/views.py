from django.shortcuts import render, redirect, HttpResponse
from .forms import ArtcleCreate_Update
# Create your views here.
from .models import Article, Comment
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def blogs_view(request):
    articles = Article.objects.all()
    return render(request, 'homepage.html', {'articles': articles})

@login_required
def create(request):
    if request.method == 'POST':
        form = ArtcleCreate_Update(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            thumbnail = form.cleaned_data['thumbnail']
            author = request.user.profile
            published = form.cleaned_data['published']
            Article.objects.create(title=title, content=content, thumbnail=thumbnail, author=author, published=published)
            return redirect('blogs_view')

    form = ArtcleCreate_Update()
    return render(request, 'create_blog.html', {'form':form})

@login_required
def update(request, uid):
    blog = Article.objects.filter(aid=uid)
    if blog and request.user== blog[0].author:
        blog = blog[0]
        if request.method == 'POST':
            form = ArtcleCreate_Update(request.POST, request.FILES)
            if form.is_valid():
                title = form.cleaned_data['title']
                content = form.cleaned_data['content']
                thumbnail = form.cleaned_data['thumbnail']
                published = form.cleaned_data['published']
                blog.title = title
                blog.content = content
                blog.thumbnail = thumbnail
                blog.published = published
                blog.save()
                return redirect('blogs_view')
        form = ArtcleCreate_Update(instance=blog)
        return render(request, 'create_blog.html', {'form': form})
    else:
        return HttpResponse('Bad Request')

@login_required
def add_comment(request):
    if request.is_ajax and request.method == "POST":
        user = request.user
        comment = request.POST.get('comment', None)
        uid = request.POST.get('uid', None)
        Comment.objects.create(commentText=comment, commenter=user, commentOn=Article.objects.get(aid=uid))
        data = {
            'status': 'success'
        }
        # calculate the result
        # print(JsonResponse(data))
        return JsonResponse(data)

@login_required
def add_rm_like(request):
    if request.is_ajax and request.method == "POST":
        user = request.user
        liked = request.POST.get('liked', None)
        uid = request.POST.get('uid', None)
        comment = Comment.objects.get(cid=uid)
        if liked:
            comment.likes.add(user)
            comment.save()
        elif not liked:
            comment.likes.remove(user)
            comment.save()
        data = {
            'status': 'success'
        }
        # calculate the result
        # print(JsonResponse(data))
        return JsonResponse(data)







