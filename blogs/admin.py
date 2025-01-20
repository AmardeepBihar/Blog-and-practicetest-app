from django.contrib import admin
from .models import BlogsModel,Catogery,ContactQuery,Feedback,MCQ_Question
from django.contrib.auth.models import User
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class ContactQueryAdmin(ImportExportModelAdmin,admin.ModelAdmin):
  list_display = ("subject", "name", "email",)
  prepopulated_fields = {"slug": ["subject"]}
admin.site.register(ContactQuery,ContactQueryAdmin)

class BlogModelAdmin(ImportExportModelAdmin,admin.ModelAdmin):
  list_display = ("title", "catogery",'author', "published_date",)
  prepopulated_fields = {"slug": ["title"]}
  list_filter = ('title','catogery','author','published_date')
  search_fields = ['title','catogery','author','description']
admin.site.register(BlogsModel,BlogModelAdmin)

class MCQ_QuestionAdmin(ImportExportModelAdmin,admin.ModelAdmin):
  list_display = ("question", "catogery")
  list_filter = ("question", "catogery")
  search_fields = ["question", "catogery"]
admin.site.register(MCQ_Question,MCQ_QuestionAdmin)

class CatogeryAdmin(ImportExportModelAdmin,admin.ModelAdmin):
  list_display = ["name"]
  list_filter = ['name']
  search_fields = ['name']
  prepopulated_fields = {"slug":["name"]}
admin.site.register(Catogery,CatogeryAdmin)

class FeedbackAdmin(ImportExportModelAdmin,admin.ModelAdmin):
  list_display = ("overall_experiance",'content_quality', "description_of_issue",)
  prepopulated_fields = {"slug": ['description_of_issue']}
admin.site.register(Feedback,FeedbackAdmin)

