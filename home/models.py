from django.db import models
from django.contrib.auth.models import User
# # Create your models here.

# Creating a custom user model and link wuth default user models


class Custom_User(models.Model):
    id_no = models.AutoField(primary_key=True, unique=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    userimage = models.ImageField(
        upload_to="userImage", default='userImage/01.jpg')
    mobileno = models.CharField(max_length=20, default="")
    profession = models.CharField(max_length=100, default="")
    userbio = models.TextField(max_length=222)
    address = models.TextField(default='Earth')
    link_linkedin = models.CharField(
        max_length=10000, null=True, blank=True, default="")
    link_facebook = models.CharField(
        max_length=10000, null=True, blank=True, default="")
    link_insta = models.CharField(
        max_length=10000, null=True, blank=True, default="")
    link_youtube = models.CharField(
        max_length=10000, null=True, blank=True, default="")
    link_website = models.CharField(
        max_length=10000, null=True, blank=True, default="")
    link_twitter = models.CharField(
        max_length=10000, null=True, blank=True, default="")


# Save the faqs here
class Faq(models.Model):
    id_no = models.AutoField(primary_key=True, unique=True)
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question


# Specifing Choice field
# Specifing the post of a team member
Post_Choice = (
    ("CEO", "1 CEO"),
    ("Product Manager", "2 Product Manager"),
    ("Accountent", "3 Accountent"),
    ('Assistent Manager', "4 Assistent Manager"),
)

# Specifing the ratings of a team member
Ratings_Choice = [
    ("d", "1"),
    ("dy", "2"),
    ("dty", "3"),
    ("dhyf", "4"),
    ("dykfg", "5"),
]

# Enter the details of a team member


class Team_Member(models.Model):
    id_no = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    post = models.CharField(max_length=100, choices=Post_Choice, default='CEO')
    image = models.ImageField(upload_to="team/")
    ratings = models.CharField(
        max_length=10, choices=Ratings_Choice, default='1')
    bio = models.TextField()

# Save the contact details and messages to reply them later


class Contact(models.Model):
    id_no = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=1000)
    message = models.TextField()
    date = models.DateField(auto_now_add=True)

# Save the email to give them notificaton of the upcoming new blog


class Subscribe(models.Model):
    id_no = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.email

# Save the all blogs content here


class Blog(models.Model):
    id_no = models.AutoField(primary_key=True, unique=True)
    title = models.CharField(max_length=1000)
    content = models.TextField()
    image = models.ImageField(upload_to="blogImage")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    date = models.TextField(max_length=100)
    slug = models.SlugField(null=False, unique=True)

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = f"{self.title[0:1000]}-{self.category}"
        return super().save(*args, **kwargs)


class Comment(models.Model):
    id_no = models.AutoField(primary_key=True, unique=True)
    master = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, related_name="+")
    uploader = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    parent_blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.TextField(max_length=100)
