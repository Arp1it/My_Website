from django.shortcuts import render, redirect, HttpResponse
from . models import BlogPost, Blogcomment
from django.contrib import messages
# from maiinn.models import userProfile
# from maiinn.forms import ImageForm

# Create your views here.
def bloghome(request):
    posts = BlogPost.objects.all()

    # print(posts)
    context = {"posts":posts}
    return render(request, "blog/bloghome.html", context)

def blogpost(request, slug):
    blposts = BlogPost.objects.filter(slugg=slug).first()



    comments = Blogcomment.objects.filter(post=blposts, parent=None)

    com= Blogcomment.objects.all().last()
    # print(com)

    replies = Blogcomment.objects.filter(post=blposts).exclude(parent=None)

    repldit = {}
    for reply in replies:
        if reply.parent.sno not in repldit:
            repldit[reply.parent.sno] = [reply]

        else:
            repldit[reply.parent.sno].append(reply)

    contextt = {"post":blposts, "comments":comments, "replydict":repldit, "com":com}
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

def search(request):
    if request.method == "GET":
        que = request.GET['query']
        print(que)

        if len(que) > 30:
            return render(request, "blog/search.html", {"query":que})

        if len(que) < 4:
            return render(request, "blog/search.html", {"query":que})

        q = BlogPost.objects.filter(content__icontains=que)
        q1 = BlogPost.objects.filter(author__icontains=que)
        q2 = BlogPost.objects.filter(mainhead__icontains=que)
        q3 = BlogPost.objects.filter(aboutauthor__icontains=que)
        qqq = q.union(q1, q2, q3)
        # q = BlogPost()
        # print(q)


        return render(request, "blog/search.html", {"qqq":qqq, "query":que})

        # else:
        #     return HttpResponse("hey")