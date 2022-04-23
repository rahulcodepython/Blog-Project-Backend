from django.contrib import admin
from home.models import Custom_User, Faq, Team_Member, Contact, Subscribe, Blog, Comment
# Register your models here.

class Team_Admin(admin.ModelAdmin):
    model = Team_Member
    list_display = ['name', 'id_no', 'post', 'ratings']

class Contact_Admin(admin.ModelAdmin):
    model = Contact
    list_display = ['name', 'id_no', 'subject']

class Custom_User_Admin(admin.ModelAdmin):
    model = Custom_User
    list_display = ['username', 'id_no', 'profession']

class BlogAdmin(admin.ModelAdmin):
    model = Blog
    list_display = ['author', 'title', 'id_no', 'date']

class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ['uploader', 'parent_blog', 'id_no',]
    
admin.site.register(Custom_User, Custom_User_Admin)
admin.site.register(Faq)
admin.site.register(Team_Member, Team_Admin)
admin.site.register(Contact, Contact_Admin)
admin.site.register(Subscribe)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)