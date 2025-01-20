from django import forms
from .models import Catogery,BlogsModel,Feedback

# CATOGERY FORM
class CatogeryModelForm(forms.ModelForm):
    class Meta:
        model = Catogery
        fields = ['name']
        wedgets = {
            'name':forms.TextInput(attrs={'class':'form-control'})
        }
        
# BLOG POST FORM
class BlogModelForm(forms.ModelForm):
    class Meta:
        model = BlogsModel
        fields = ['title','catogery','author','description','blog_list_image','detail_image']
        wedgets = {
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'catogery':forms.Select(attrs={'class':'form-control'}),
            'author':forms.Select(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control'}),
            'blog_list_image':forms.TextInput(attrs={'class':'form-control'}),
            'detail_image':forms.TextInput(attrs={'class':'form-control'})
        }

# FEEDBACK FORM
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = (
            'overall_experiance', 
            'content_quality', 
            'design_usability',
            'most_enjoyable_thing', 
            'suggestions', 
            'encountered_any_issues',
            'description_of_issue', 
            'additional_comment'
        )
        widgets = {
            'description_of_issue':forms.Textarea(attrs={'class':'form-control'}),
            'additional_comment':forms.Textarea(attrs={'class':'form-control'}),
            'suggestions':forms.Textarea(attrs={'class':'form-control'}),
            'most_enjoyable_thing':forms.Textarea(attrs={'class':'form-control'}),
            'overall_experiance':forms.Select(attrs={'class':'form-control'}),
            'content_quality':forms.Select(attrs={'class':'form-control'}),
            'design_usability':forms.Select(attrs={'class':'form-control'}),
            'encountered_any_issues':forms.Select(attrs={'class':'form-control'}),
        }
      