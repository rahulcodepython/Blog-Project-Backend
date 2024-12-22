from django.contrib import admin
from django.urls import path
from . import settings
from django.conf.urls.static import static

# home app rendering setting
from home.views import index, contact, register_user, login_user, logout_user, allblogposts, blogcontent, blog_upload_template, blog_upload, postcomment, deletecomment

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Home APIs
    path('', index, name="index"),
    path('contact/', contact, name='contact'),
    path('allblogposts/<filter>', allblogposts, name="allblogposts"),
    path('blogcontent/<slug>', blogcontent, name="blogcontent"),
    path('blog_upload_template/', blog_upload_template, name="blog_upload_template"),
    path('blog_upload/', blog_upload, name="blog_upload"),
    path('postcomment/', postcomment, name="postcomment"),
    path('deletecomment/<id>', deletecomment, name="deletecomment"),

    # Authentication APIs
    path('register_user/', register_user, name='register_user'),
    path('login_user/', login_user, name='login_user'),
    path('logout_user/', logout_user, name='logout_user'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
