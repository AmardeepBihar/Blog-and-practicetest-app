
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from .models import BlogsModel,Catogery,ContactQuery,Feedback,MCQ_Question
from .forms import CatogeryModelForm,BlogModelForm,FeedbackForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import datetime
from django.utils import timezone
import random
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def Blogs(request):
    today = timezone.now().date()
    blog_posts = BlogsModel.objects.exclude(published_date__date=today).order_by('-published_date')
    slides = BlogsModel.objects.filter(published_date__date=today)
    pag = Paginator(blog_posts,6) # This is paginator method which manages the pages
    page = request.GET.get('page')
    pages = pag.get_page(page)  
    cat_manu = Catogery.objects.all()
    template = 'blog/index.html'
    data = {'cat_manu':cat_manu,'pages':pages,'slides':slides}
    return render(request, template,data)

#quiz related view
def QuizList(request):
    question  = MCQ_Question.objects.all()
    # Shuffle the questions randomly
    question_mcq = list(question)
    random.shuffle(question_mcq)
     # Apply pagination to the shuffled questions
    pag = Paginator(question_mcq,20)
    page = request.GET.get('page')
    pages = pag.get_page(page) 
    cat_manu = Catogery.objects.all()
    data = {'question_mcq': question_mcq,'pages':pages,'cat_manu':cat_manu}
    return render(request,'mcq/quiz-list.html',data)


def QuizDiscussion(request, uid):
    ans = get_object_or_404(MCQ_Question, uid=uid)
    all_mcq = MCQ_Question.objects.all()
    cat_manu = Catogery.objects.all()
    obje = MCQ_Question.objects.exclude(uid=ans.uid)
    # List of options to randomize
    options = [ans.option1, ans.option2, ans.option3, ans.option4]
    random.shuffle(options) 
    # Get the next random question
    correct_answer_position = options.index(ans.correct_ans)
    # Find the new position of the correct answer after shuffling the options
    next_question = random.choice(all_mcq)  # This will give 0 for option1, 1 for option2, etc.
    
    # Initialize session variables if not already set
    if 'attempted_questions' not in request.session:
        request.session['attempted_questions'] = 0
        request.session['correct_answers'] = 0
        request.session['incorrect_answers'] = 0

    data = {
        'ans': ans,
        'next_question': next_question,
        'options': options,
        'correct_answer_position': correct_answer_position,
        'random_question': random.sample(list(all_mcq), min(5, len(all_mcq))),
        'cat_manu': cat_manu,
        'obje': obje
    }
    return render(request, 'mcq/quiz-descussion.html', data)

# this view is only to capture the session of the broweser to make the report of quiz.
@csrf_exempt
def UpdateSessionResults(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        selected_answer = data.get('selected_answer')
        correct_answer = data.get('correct_answer')
        # Initialize session data if not already done
        if 'attempted_questions' not in request.session:
            request.session['attempted_questions'] = 0
            request.session['correct_answers'] = 0
            request.session['incorrect_answers'] = 0
        # Increment attempted questions count
        request.session['attempted_questions'] += 1
        # Check if the selected answer is correct
        if selected_answer == correct_answer:
            request.session['correct_answers'] += 1
        else:
            request.session['incorrect_answers'] += 1
        # Mark the session as modified to save changes
        request.session.modified = True
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def ResultView(request):
    all_mcq = MCQ_Question.objects.all()
    next_question = random.choice(all_mcq)
    cat_manu = Catogery.objects.all()
    # Calculate score and display result
    attempted = request.session.get('attempted_questions', 0)
    correct = request.session.get('correct_answers', 0)
    incorrect = request.session.get('incorrect_answers', 0)
    percentage = (correct / attempted * 100) if attempted > 0 else 0
    # Calculate the percentage
    if attempted > 0:
        percentage = (correct / attempted) * 100
    else:
        percentage = 0
    result = {
        'attempted': attempted,
        'correct': correct,
        'incorrect': incorrect,
        'percentage': percentage,
        'next_question':next_question,
        'cat_manu':cat_manu
    }
    # Reset session after showing result
    request.session.flush()
    return render(request, 'mcq/result.html', result)



def CategoriesWiseQuestion(request,slug):
    catogere = get_object_or_404(Catogery,slug=slug)
    post = catogere.ques.all() #here posts is the related field of blog model.
    p = Paginator(post,24)  #pagination applied
    page = request.GET.get('page')
    pages = p.get_page(page)
    cat_manu = Catogery.objects.all()
    template = 'mcq/categorywisequestion.html'
    return render(request,template,{'category':catogere,'cat_manu':cat_manu,'pages':pages})

def BlogDetail(request,slug):
    obj = get_object_or_404(BlogsModel,slug=slug)
    cat_manu = Catogery.objects.all()
    obje = BlogsModel.objects.exclude(uid=obj.uid).order_by('-published_date')[:5]
    all_blogs = BlogsModel.objects.all()
    random_blogs = random.sample(list(all_blogs), min(5, len(all_blogs))) #for show random blog
    template = 'blog/blog_detail.html'
    data = {'obj':obj,'obje':obje,'cat_manu':cat_manu, 'random_blogs':random_blogs}
    return render(request,template,data)

@login_required
def UploadBlog(request):
    if request.method == 'POST':
        form = BlogModelForm(request.POST,request.FILES)
        if form.is_valid:
            post = form.save(commit=False)
            post.author =  request.user
            post.save()
            messages.success(request,'Blog has been posted successfully!')
            return redirect('home')
    else:
        form = BlogModelForm()
    return render(request,'blog/blog_post.html',{'form':form})

def Deleteblog(request,slug):
    post = get_object_or_404(BlogsModel,slug=slug)
    post.delete()
    messages.info(request,'Post deleted successful.')
    return redirect('home')

def Categories(request,slug):
    catogere = get_object_or_404(Catogery,slug=slug)
    post = catogere.posts.all() #here posts is the related field of blog model.
    p = Paginator(post,6)  #pagination applied
    page = request.GET.get('page')
    pages = p.get_page(page)
    cat_manu = Catogery.objects.all()
    template = 'blog/category.html'
    return render(request,template,{'category':catogere,'cat_manu':cat_manu,'pages':pages})



def SearhcKey(request):
    if request.method == 'POST':
        search = request.POST.get('search', '').strip()  # Get search input and strip whitespace
        if not search:  # Check if the search term is empty
            return redirect('home')  # Redirect to the home page
        else:
            # Filter items based on the search term
            items = BlogsModel.objects.filter(description__icontains=search) | BlogsModel.objects.filter(title__icontains=search)
            p = Paginator(items, 6)  # Apply pagination
            page = request.GET.get('page')
            pages = p.get_page(page)
            cat_manu = Catogery.objects.all()
            data = {'search': search, 'cat_manu': cat_manu, 'pages': pages}
            return render(request, 'blog/search_page.html', data)
    else:
        # For GET requests, you can also choose to redirect or render an empty search page
        return render(request, 'blog/search_page.html', {})





# CONTACT VIEW
def Contact(request):
    cat_manu = Catogery.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        subject = request.POST['subject']
        query = request.POST['query']
        data  = ContactQuery(name=name,phone=phone,email=email,subject=subject,query=query)
        data.save()
        messages.info(request,'Query has been submited, we will connect you soon! Thank you')
        return redirect('/')
    template = 'contact-us/contact.html'
    return render(request, template,{'cat_manu':cat_manu})


def About(request):
    cat_manu = Catogery.objects.all()
    template = 'about-us/about.html'
    return render(request, template,{"cat_manu":cat_manu})

def DeclarationPage(request):
    cat_manu = Catogery.objects.all()
    template = 'other-app/declaration.html'
    return render(request,template,{"cat_manu":cat_manu})

def PrivacyPolicy(request):
    cat_manu = Catogery.objects.all()
    template = 'other-app/privacy-policy.html'
    return render(request,template,{"cat_manu":cat_manu})

def Feedback(request):
    cat_manu = Catogery.objects.all()
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request,'Thank you for submiting your valuable view with us.')
            return redirect('/')  # Redirect to a success page
    else:
        form = FeedbackForm()
    return render(request, 'other-app/feedback.html', {'form': form,"cat_manu":cat_manu})

def AuthorDetail(request):
    template = 'admin/authordetail.html'
    author = User.objects.all()
    return render(request, template,{'author':author})

