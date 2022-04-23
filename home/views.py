from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from home.models import Faq, Team_Member, Contact, Subscribe, Custom_User, Blog, Comment
from django.db.models import Q
from datetime import date
today = date.today()

# # Create your views here.

# Function for showing the logged in user info
@login_required
def show_user_info(request):
    custom_user_info = Custom_User.objects.get(username=request.user)
    return custom_user_info

# Function for automated subscribing website using email
def auto_subscribe(email, user):
    user_email_save = Subscribe(email=email, user=user, )
    user_email_save.save()

# Count the number of blogs of a particular catagories
def blog_category_name_count():
    category_blog_count = {
        "General": Blog.objects.filter(category="General").count(),
        "Tech": Blog.objects.filter(category="Tech").count(),
        "Blog": Blog.objects.filter(category="Blog").count(),
        "News": Blog.objects.filter(category="News").count(),
        "Lifestyle": Blog.objects.filter(category="Lifestyle").count(),
        "Education": Blog.objects.filter(category="Education").count(),
        "Travel": Blog.objects.filter(category="Travel").count(),
        "Art": Blog.objects.filter(category="Art").count(),
        "Households": Blog.objects.filter(category="Households").count(),
        "Others": Blog.objects.filter(category="Others").count(),
    }
    return category_blog_count

# Render the main page
def index(request):
    # Home Models

    # Frequently Asked Question section
    faqs = Faq.objects.all()

    # List of team members
    teammebers = Team_Member.objects.all().order_by('-ratings')

    # Logged in user image show
    user_info = show_user_info(request)

    # Fetch maximum three blog
    blogCount = Blog.objects.all().count()
    if (blogCount>=1):
        blogsItems = Blog.objects.all().order_by('-date')[:3]
        contextBlogItems = {
            'blogs': blogsItems, 
            'faqs': faqs, 
            'teams': teammebers,
            'user_info': user_info, 
            }
    else:
        contextBlogItems = {
            'faqs': faqs, 
            'teams': teammebers,
            'user_info': user_info, 
            }

    return render(request, "index.html", contextBlogItems)

# Save the contact form data to database
def contact(request):
    if request.method=="POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        contact = Contact(name=name, email=email, subject=subject, message=message)
        contact.save()

        messages.success(request, "Hurrah! Your message have been recieved.")
        return render(request, 'index.html')

    else:
        messages.error(request, "Sorry! Your message have not been recieved. Try again.")
        return redirect("/#contact")

# Show all blogs
def allblogposts(request, filter):

    # Logged in user image show
    user_info = show_user_info(request)

    # Fetch maximum three blog
    recent_blogs = Blog.objects.all().order_by('-id_no')[:10]

    # Call the function to print the number of blogs of a particular category with category name
    blog_category_name_count_s = blog_category_name_count()
    
    # Fetching all blogs
    if filter=='new':
        blogPosts = Blog.objects.all().order_by('-id_no')

    elif filter=='old':
        blogPosts = Blog.objects.all().order_by('id_no')

    elif filter=='popular':
        blogPosts = Blog.objects.all()

    elif filter=='query':
        if request.method == "POST":
            query = request.POST.get('search_query').capitalize()
        else:
            query = ""

        blogPosts = Blog.objects.filter(Q(title__icontains = query)).order_by('-id_no')

    else: 
        blogPosts = Blog.objects.filter(category=filter).order_by('-id_no')
    
    # Count quantity of all blogs
    blogs_count = Blog.objects.all().count()

    context_blogPosts = {
        'blogs': blogPosts,
        'allblogs_count': blogs_count,
        'user_info': user_info, 
        'recent_blogs': recent_blogs,
        'counts': blog_category_name_count_s,
    }
    return render(request, "allblogposts.html", context_blogPosts)

# Sent to a specific blog to read it
def blogcontent(request, slug):

    # Logged in user image show
    user_info = show_user_info(request)

    # Fetch particular blog information
    blogPost = Blog.objects.get(slug = slug)

    # Fetch the id of the blog
    id = blogPost.id_no
    
    # Fetch the author data of the blog
    author = Custom_User.objects.get(username=blogPost.author)

    # Sent the current user info
    if request.user.is_authenticated:
        user = Custom_User.objects.get(username=request.user)
    else:
        user = []

    # Call the function to print the number of blogs of a particular category with category name
    blog_category_name_count_s = blog_category_name_count()

    # Fetch Comments
    comments = Comment.objects.filter(parent_blog = id, master=None)
    comment_count = Comment.objects.filter(parent_blog = id).count()

    # Fetching the replies

    comment_reply = []
    for comment in comments:
        replies = Comment.objects.filter(master = comment)
        comment_reply.append([comment, replies])

    # Fetch maximum three blog
    recent_blogs = Blog.objects.all().order_by('-date')[:10]

    # Count quantity of all blogs
    allblogs_count = Blog.objects.all().count()

    context_blogPost = {
        'blog': blogPost,
        'allblogs_count': allblogs_count,
        'comments': comments,
        'comment_count': comment_count,
        'user_info': user_info,
        'author': author,
        'userid': user,
        'recent_blogs': recent_blogs,
        'counts': blog_category_name_count_s,
        'comment_reply': comment_reply,
    }
    return render(request, "blogcontent.html", context_blogPost)

def blog_upload_template(request):

    # Logged in user image show
    user_info = show_user_info(request)

    context = {
        'user_info': user_info, 
    }

    return render(request, "blogwritting.html", context)

# Upload the new blog posts
@login_required
def blog_upload(request):
    if request.method == 'POST':
        title = request.POST.get('title').capitalize()
        image = request.FILES['image']
        category = request.POST.get('category').capitalize()
        content = request.POST.get('content').capitalize()
        author = request.user
        date = today.strftime("%B %d, %Y")
        
        blog_save = Blog(title=title, image=image, content=content, author=author, category=category, date=date)
        blog_save.save()

        # Redirect to that blog
        uploaded_blog = Blog.objects.get(title=title)
        blog_slug = uploaded_blog.slug

        messages.success(request, "You have successfully uploaded a new blog.")
        return redirect(blogcontent, blog_slug)
    else:
        messages.error(request, "Blog is not successfully uploaded, try again.")
        return redirect(blog_upload_template)

@login_required
# Save comments of a blog
def postcomment(request):
    if request.method=='POST':
        id_blog_no = request.POST.get('id_blog_no')
        id_user_no = request.POST.get('id_user_no')
        parent_comment = request.POST.get('parent_comment')
        comment = request.POST.get('comment').capitalize() 
        parent_blog = Blog.objects.get(id_no=id_blog_no)
        uploader = Custom_User.objects.get(id_no=id_user_no)
        date = today.strftime("%B %d, %Y")
        
        if parent_comment == "":
            comment_save = Comment(uploader=uploader, comment=comment, parent_blog=parent_blog, date=date)
            comment_save.save()

            messages.success(request, "Your comment is posted.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        else:
            master = Comment.objects.get(id_no=parent_comment)
            comment_save = Comment(uploader=uploader, comment=comment, parent_blog=parent_blog, master=master, date=date)
            comment_save.save()

            messages.success(request, "Your reply is posted.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    else:
        messages.error(request, "You did not post the comment properly.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# Delete the comment by the user
def deletecomment(request, id):
    delete_comment = Comment.objects.get(id_no=id)
    delete_comment.delete()
    messages.success(request, "Your comment has been deleted.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# Save the data of registration form and make a new user
def register_user(request):
    if request.method=='POST':
        firstname = request.POST.get('firstname').capitalize()
        lastname = request.POST.get('lastname').capitalize()
        username = request.POST.get('username')
        email = request.POST.get('email')
        image = request.FILES['image']
        number = request.POST.get('number')
        bio = request.POST.get('bio').capitalize()
        address = request.POST.get('address')
        password = request.POST.get('password')
        profession = request.POST.get('profession').capitalize()
        facebook = request.POST.get('facebook')
        insta = request.POST.get('insta')
        youtube = request.POST.get('youtube')
        linkedin = request.POST.get('linkedin')
        website = request.POST.get('website')
        twitter = request.POST.get('twitter')

        # Django build-in user save
        user_info_default = User.objects.create_user(first_name=firstname, last_name=lastname, username=username, email=email, password=password)
        user_info_default.save()

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                
                # Custom User save
                custom_username = request.user
                user_info_custom = Custom_User(userbio=bio, mobileno=number, address=address, userimage=image, username=custom_username, profession=profession, link_facebook=facebook, link_insta=insta, link_linkedin=linkedin, link_twitter=twitter, link_website=website, link_youtube=youtube)
                user_info_custom.save()

                # Newsletter Save
                subscribe = Subscribe(email=email, user=request.user)
                subscribe.save()

        # Logged in user image show
        user_info = show_user_info(request)

        messages.success(request, f"Hurrah! You have registerd and logged in as {username}.")

        context = {
            'user_info': user_info, 
        }

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, "Sorry! You are not properly registerd. Try again.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# Log in a preregistered user
def login_user(request):
    if request.method=='POST':
        email_user = request.POST.get('email')
        password_user = request.POST.get('password')

        if (User.objects.filter(email=email_user)):
            user_email_info = User.objects.filter(email=email_user).first()
            username_user = user_email_info.username
        else:
            messages.error(request, "Sorry! There is no such email")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user = authenticate(username=username_user, password=password_user)

        if user is not None:
            if user.is_active:
                login(request, user)

                # Logged in user image show
                user_info = show_user_info(request) 

                messages.success(request, f"Hurrah! You are logged in as { username_user }.")
                    
                context = {
                    'user_info': user_info, 
                }

                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            else:
                messages.error(request, "Sorry! You are not active. False login is denied. Try again.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
        else:
            messages.error(request, f"Sorry! There are no such user like {username_user}. Try again.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, "Sorry! You are not log in properly. Try again.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# Log out the logged in user
@login_required
def logout_user(request):
    print('logged out')
    logout(request)

    messages.success(request, "You are successfully logged out.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))