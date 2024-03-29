from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from . models import BlogPost, Blogcomment, BlogLike, BlogViews
from django.contrib import messages
# from maiinn.models import userProfile
# from maiinn.forms import ImageForm

# Create your views here.
def bloghome(request):
    posts = BlogPost.objects.order_by('-views', '-time')

    # print(posts)
    context = {"posts":posts}
    return render(request, "blog/bloghome.html", context)

def blogpost(request, slug):
    blposts = BlogPost.objects.filter(slugg=slug).first()

    print(f"{blposts.author} - {blposts.mainhead}")

    if request.user.is_authenticated:
        user = request.user

        btlv = BlogViews.objects.filter(user=user, asss=blposts).first()
        # print(btlv == None)
        # print(btlv)
        # # print(btlv.user)
        # print((str(btlv.asss)))
        # print(blposts)
        # print(str(btlv.asss) != str(blposts))
        h = blposts.sno
        hhv = BlogPost.objects.get(sno=h)
        # print(hhv)

        if btlv != None:
            if btlv.asss != blposts: 
                ssv = BlogViews(user=user, asss=hhv)
                ssv.save()
                blvi = len(BlogViews.objects.filter(asss=blposts))
                v = BlogPost.objects.get(slugg__exact=slug)
                v.views = int(blvi)
                v.save()
        if btlv == None:
            ssv = BlogViews(user=user, asss=hhv)
            ssv.save()
            blvi = len(BlogViews.objects.filter(asss=blposts))
            v = BlogPost.objects.get(slugg__exact=slug)
            v.views = int(blvi)
            v.save()

    blvi = len(BlogViews.objects.filter(asss=blposts))

    blogl = len(BlogLike.objects.filter(assspost=blposts))

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

    contextt = {"post":blposts, "comments":comments, "replydict":repldit, "com":com, "likes":blogl, "view":blvi}
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
    # return HttpResponse("404 - Not Found")

def editpost(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            snoo = request.POST['snopost']
            ed = BlogPost.objects.filter(sno=snoo)
            # print(snoo, ed)
            return render(request, "blog/editpost.html", {"posts":ed})
    return HttpResponse("404 - Not Found")

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
    return HttpResponse("404 - Not Found")

def comdel(request):
    if request.method == "POST":
        comsnodel = request.POST['snocomdel']
        slugggy = request.POST['slugggy']
        # print(comsnodel, slugggy)

        cred = get_object_or_404(Blogcomment, sno=comsnodel)
        cred.delete()
        return redirect(f"/blog/{slugggy}")

    return HttpResponse("404 - Not Found")

def bloglike(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            user = request.user
            postlikesno = request.POST['Postlikesno']
            post = BlogPost.objects.get(sno=postlikesno)
            sl = request.POST['likesl']

            l = set()

            students = BlogLike.objects.select_related('user')
            for stud in students:
                l.add(stud.user.username)

            print(list(l))

            asspos = list(BlogLike.objects.values_list("assspost", flat=True))
            print(asspos, user)
            print(postlikesno)
            print(str(user)in l)
            print(int(postlikesno) in asspos)

            if str(user) in l and int(postlikesno) in asspos:
                creed = get_object_or_404(BlogLike, user=user, assspost=postlikesno)
                print(creed)
                creed.delete()
                return redirect(f"/blog/{sl}")

            li = BlogLike(user=user, assspost=post)
            li.save()
            return redirect(f"/blog/{sl}")
    
    else:
        messages.error(request, "Please go and signin")
        return redirect("signin")