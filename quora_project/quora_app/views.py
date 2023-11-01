from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm,SignUpForm,LoginForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm



def home(request):
    questions = Question.objects.all().order_by('-created_at')
    answers = Answer.objects.all()  # Fetch all answers
    return render(request, 'home.html', {'questions': questions, 'answers': answers})

def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('home')
    else:
        form = QuestionForm()
    return render(request, 'ask_question.html', {'form': form})

def answer_question(request, question_id):
    question = Question.objects.get(id=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            return redirect('home')
    else:
        form = AnswerForm()
    return render(request, 'answer_question.html', {'form': form, 'question': question})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect to the desired page after a successful login
            return redirect('home')  
    else:
        form = AuthenticationForm()
    return render(request, 'custom_login.html', {'form': form})


@login_required
def like_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    # Check if the user has already liked the answer
    if request.user in answer.likes.all():
        answer.likes.remove(request.user)  # Unlike the answer
    else:
        answer.likes.add(request.user)  # Like the answer

    return redirect('home')  

from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout(request):
    logout(request)
    return redirect('login')

