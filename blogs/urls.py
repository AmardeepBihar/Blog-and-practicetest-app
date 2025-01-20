from django.urls import path
from . import views
from django.contrib import admin
admin.site.site_header = 'Rams Administration'
admin.site.site_title = "Ram's Blog Login"
admin.site.index_title = 'Welcome to this Portal'
urlpatterns = [
    path('', views.Blogs, name='home'),
    path('blog/new-blog-post', views.UploadBlog, name='blog_post'),
    path('category/<slug:slug>/', views.Categories, name='category'),
    path('post/<slug:slug>/', views.BlogDetail, name='post_detail'),
    path('search-posts', views.SearhcKey, name='searched-key'),
    path('post-deleted/<slug:slug>', views.Deleteblog, name='delete-post'),
    path('contact/', views.Contact, name='contact'),
    path('about/', views.About, name='about'),
    path('declaration/', views.DeclarationPage, name='declaration'),
    path('privacy-policy/', views.PrivacyPolicy, name='privacyandpolicy'),
    path('feedback/', views.Feedback, name='feedback'),
    path('author-detail/', views.AuthorDetail, name='author-detail'),
    path('quiz-list/', views.QuizList, name='quiz-list'),
    path('endpractice/', views.ResultView, name='endpractice'),
    path('update_session_results/', views.UpdateSessionResults, name='update_session_results'),
    path('question/<uuid:uid>/', views.QuizDiscussion, name='ansthequestion'),
    path('category-wise-question/<slug:slug>/', views.CategoriesWiseQuestion, name='category-wise-question'),
    
]   