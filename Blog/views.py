from django.shortcuts import render, redirect, HttpResponse
from .forms import ArtcleCreate_Update, Artcle_Update
# Create your views here.
from .models import Article, Comment, Notification
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



def blogs_view(request, uid):
    article = Article.objects.get(aid=uid)
    return render(request, 'homepage.html', {'article': article})

def categoryblog(request):
    articles = Article.objects.all()
    return render(request, 'categoryblogs.html', {'articles': articles})

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
            return redirect('all')

    form = ArtcleCreate_Update()
    return render(request, 'create_blog.html', {'form':form})

@login_required
def update(request, uid):
    blog = Article.objects.filter(aid=uid)
    if blog and request.user.profile == blog[0].author:
        blog = blog[0]
        print(request.method)
        if request.method == 'POST':
            form = Artcle_Update(request.POST, request.FILES)
            print(form.errors)
            if form.is_valid():
                title = form.cleaned_data['title']
                content = form.cleaned_data['content']
                if form.cleaned_data['thumbnail']:
                    thumbnail = form.cleaned_data['thumbnail']
                    blog.thumbnail = thumbnail
                published = form.cleaned_data['published']
                blog.title = title
                blog.content = content
                blog.published = published
                blog.save()
                return redirect('all')
        form = Artcle_Update(instance=blog, initial={'content': blog.content, 'thumbnail': blog.thumbnail})
        return render(request, 'create_blog.html', {'form': form})
    else:
        return HttpResponse('Bad Request')

@login_required
@csrf_exempt
def add_comment(request):
    if request.is_ajax and request.method == "POST":
        user = request.user.profile
        comment = request.POST.get('comment', None)
        uid = request.POST.get('uid', None)[2:]
        article = Article.objects.get(aid=uid)
        Comment.objects.create(commentText=comment, commenter=user, commentOn=article)
        Notification.objects.create(type='commented', msg='commented on your blog', notifiedOn=article,
                                    noti_for=article.author, noti_by=user)
        data = {
            'status': 'success'
        }
        # calculate the result
        # print(JsonResponse(data))
        return JsonResponse(data)

@login_required
@csrf_exempt
def add_rm_like(request):
    if request.is_ajax and request.method == "POST":
        user = request.user.profile
        #liked = request.POST.get('liked', None)
        uid = request.POST.get('uid', None)
        comment = Comment.objects.get(cid=uid[1:])
        if user not in comment.likes.all():
            comment.likes.add(user)
            comment.save()
            Notification.objects.create(type='like', msg='Your comment was liked', notifiedOn=comment.commentOn, noti_for=comment.commenter, noti_by=user)
        else:
            comment.likes.remove(user)
            comment.save()
        data = {
            'status': 'success'
        }
        # calculate the result
        # print(JsonResponse(data))
        return JsonResponse(data)

@csrf_exempt
def starRate(request):
    if request.is_ajax and request.method == "POST":
        user = request.user.profile
        rated = request.POST.get('rate', None)
        uid = request.POST.get('uid', None)
        article = Article.objects.get(aid=uid[1:])
        print(float(article.rating))
        if user not in article.raters.all():
            print('inside')
            cnt = int(article.raters.all().count())
            article.rating = (((cnt*(float(article.rating)))+int(rated))/(cnt+1))
            article.raters.add(user)
            article.save()
            Notification.objects.create(type='starRating', msg='Your blog was rated', notifiedOn=article, noti_for=article.author, noti_by=user)
        else:
            return HttpResponse('U have already rated')
        data = {
            'status': 'success'
        }
        # calculate the result
        # print(JsonResponse(data))
        return JsonResponse(data)

from django.core.serializers import serialize

@csrf_exempt
def replies(request):
    if request.is_ajax and request.method == "POST":
        cid = request.POST.get('cid', None)
        data = {
            'replies': serialize("json", Comment.objects.filter(replyTo=cid[1:]))
        }
        #print(data)
        #print(JsonResponse(data))
        return JsonResponse(data)

@csrf_exempt
def savereply(request):
    if request.is_ajax and request.method == "POST":
        user = request.user.profile
        cid = request.POST.get('cid', None)
        reply = request.POST.get('reply', None)
        commenton = Comment.objects.get(cid=cid[1:])
        Comment.objects.create(commentText=reply, commenter=user, replyTo=cid[1:], commentOn=commenton.commentOn)
        Notification.objects.create(type='commented', msg='Replied to your comment', notifiedOn=commenton.commentOn,
                                    noti_for=commenton.commenter, noti_by=user)

        data = {
            'replies': reply
        }
        return JsonResponse(data)


#todo adding replies to databse and showing





