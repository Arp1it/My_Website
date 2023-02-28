from django.shortcuts import render, redirect
from . models import BlogPost, Blogcomment
from django.contrib import messages

# Create your views here.
def bloghome(request):
    posts = BlogPost.objects.all()

    # print(posts)
    context = {"posts":posts}
    return render(request, "blog/bloghome.html", context)

def blogpost(request, slug):
    blposts = BlogPost.objects.filter(slugg=slug).first()


    comments = Blogcomment.objects.filter(post=blposts, parent=None)

    replies = Blogcomment.objects.filter(post=blposts).exclude(parent=None)

    repldit = {}
    for reply in replies:
        if reply.parent.sno not in repldit:
            repldit[reply.parent.sno] = [reply]

        else:
            repldit[reply.parent.sno].append(reply)

    contextt = {"post":blposts, "comments":comments, "replydict":repldit, "image":img}
    return render(request, "blog/blogpost.html", contextt)

# API
def blogcomment(request):
    if request.method == "POST":
        commentss = request.POST['comment']
        user = request.user
        postsno = request.POST.get('PostSno')
        post = BlogPost.objects.get(sno=postsno)
        parentsno = request.POST.get("parenttssno")

        if parentsno == "":
            comments = Blogcomment(comment=commentss, user=user, post=post)
            comments.save()
            messages.success(request, "Your comment has been posted successfully")

        else:
            parrent = Blogcomment.objects.get(sno=parentsno)
            comments = Blogcomment(comment=commentss, user=user, post=post, parent=parrent)
            comments.save()
            messages.success(request, "Your comment has been posted successfully")

    return redirect(f'/blog/{post.slugg}')