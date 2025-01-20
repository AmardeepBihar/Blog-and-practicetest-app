from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
# Baseclass
class BaseClass(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    class Meta:
        abstract=True

# catogery model
class Catogery(BaseClass):
    name = models.CharField(max_length=50,null=False,unique=True)
    slug = models.SlugField(default='',null=False)
    def __str__(self):
        return f'{self.name}'

# for Blog or post model
class BlogsModel(BaseClass):
    title = models.CharField(max_length=100)
    catogery = models.ForeignKey(Catogery,on_delete=models.CASCADE,null=False,blank=False,related_name='posts')
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blogs')
    description = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    blog_list_image = models.ImageField(upload_to='static/Blog_images/ListImage')
    detail_image = models.ImageField(upload_to='static/Blog_images/detailImage')
    pdf_file = models.FileField(upload_to='static/blog_pdfs/pdf/', null=True, blank=True)
    slug = models.SlugField(default='',null=False)

    def __str__(self):
        return f'{self.title} | {self.published_date}'

# Quiz
class MCQ_Question(BaseClass):
    question = models.TextField(max_length=300)
    catogery = models.ForeignKey(Catogery,on_delete=models.CASCADE,related_name='ques')
    option1 = models.CharField(max_length=50)
    option2 = models.CharField(max_length=50)
    option3 = models.CharField(max_length=50)
    option4 = models.CharField(max_length=50)
    correct_ans = models.CharField(max_length=50)
    explanation = models.TextField(max_length=1000)
    slug = models.SlugField(default='',null=False)

    def __str__(self):
        return f'{self.question} | {self.catogery}'



# for contact query model
class ContactQuery(BaseClass):
    name = models.CharField(max_length=80)
    phone = models.CharField(max_length=10,unique=True)
    email = models.EmailField(max_length=100,unique=True)
    subject = models.CharField(max_length=100)
    query = models.TextField(max_length=500)
    slug = models.SlugField(default='',null=False)
    def __str__(self):
        return f'{self.id} | {self.name} | {self.subject}'

# for feedback model
class Feedback(BaseClass):
    FEEDBACK_CHOICE = [
        ('5','Excellent'),
        ('4','Good'),
        ('3','Average'),
        ('2','Poor'),
        ('2','Vary Poor'),
    ]
    ISSUE_OR_PROBLEM = [
        ('1','Design Problem'),
        ('2','Content Erro'),
        ('3','Bug/Technical Issue'),
        ('4','Other'),
        ('5','None'),
    ]
    overall_experiance = models.CharField(max_length=1,choices=FEEDBACK_CHOICE,default=5)
    content_quality = models.CharField(max_length=1,choices=FEEDBACK_CHOICE,default=5)
    design_usability = models.CharField(max_length=1,choices=FEEDBACK_CHOICE,default=5)
    most_enjoyable_thing = models.TextField(max_length=300)
    suggestions = models.TextField(max_length=200)
    encountered_any_issues = models.CharField(max_length=1,choices=ISSUE_OR_PROBLEM,default=5)
    description_of_issue = models.TextField(max_length=300)
    additional_comment = models.TextField(max_length=300)
    slug = models.SlugField(default='',null=False)

    def __str__(self):
        return f'{self.id} | {self.overall_experiance} | {self.content_quality} | {self.encountered_any_issues}'
    