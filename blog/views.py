from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
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

def Postblog(request):
    if request.user.is_authenticated:
        user = request.user
        blpost = BlogPost.objects.filter(user=user)
        if request.method == "POST":
            author = request.POST['auth']
            mainhead = request.POST['mainh']
            slug = request.POST['slug']
            about_author = request.POST['aboutauth']
            content = request.POST.get('content', False)
            print(content)

            slugy = list(BlogPost.objects.values_list("slugg", flat=True))
            if slug in slugy:
                messages.error(request, "Slug is already taken")
                return redirect("/blog/Postblog")

            post = BlogPost(user=user, author=author, mainhead=mainhead, content=content, slugg=slug, aboutauthor=about_author)
            post.save()
            messages.success(request, "Successfully Posted")
        return render(request, "blog/posting.html", {'posts':blpost})
    return HttpResponse("404 - Not Found")

def delet(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            sno = request.POST['snodel']
            cred = get_object_or_404(BlogPost, sno=sno)
            cred.delete()
            return redirect("/blog/Postblog")

def editpost(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            snoo = request.GET['snopost']
            ed = BlogPost.objects.filter(sno=snoo)
            # print(snoo, ed)
            return render(request, "blog/editpost.html", {"posts":ed})

def newwpos(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            author = request.POST['auth']
            mainhead = request.POST['mainh']
            slug = request.POST['slug']
            matchslug = request.POST['matchslug']
            snoo = request.POST['snoo']
            about_author = request.POST['aboutauth']
            content = request.POST.get('content', False)

            if slug != matchslug:
                sluggg1 = list(BlogPost.objects.values_list("slugg", flat=True))
                print(sluggg1)
                if slug in sluggg1:
                    messages.error(request, "Slug is already be taken")
                    return redirect(f"/blog/editpost?snopost={snoo}")

            user = request.user
            change = BlogPost.objects.get(user__exact=user)
            change.author = author
            change.mainhead = mainhead
            change.content = content
            change.slugg = slug
            change.aboutauthor = about_author
            change.save()
            messages.success(request, "Your Post had been updated.")
            return redirect("/blog/Postblog")