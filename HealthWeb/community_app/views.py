from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.contrib.auth.models import User
from .models import Question, Answer, Journey, Category, UserProfile
from .forms import (UserRegisterForm, QuestionForm,
                    AnswerForm, JourneyForm, UserProfileForm)


def home(request):
    questions = Question.objects.all().order_by('-created_at')
    trending_questions = Question.objects.annotate(
        answer_count=Count('answers')
    ).order_by('-answer_count')[:5]

    categories = Category.objects.all()

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        questions = questions.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )

    context = {
        'questions': questions[:20],  # Limit to 20 recent questions
        'trending_questions': trending_questions,
        'categories': categories,
        'search_query': search_query,
    }
    return render(request, 'community_app/home.html', context)


def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = question.answers.all().order_by('-created_at')

    if request.method == 'POST' and request.user.is_authenticated:
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.user = request.user
            answer.save()
            messages.success(request, 'Your answer has been posted!')
            return redirect('question_detail', question_id=question.id)
    else:
        form = AnswerForm()

    context = {
        'question': question,
        'answers': answers,
        'form': form,
    }
    return render(request, 'community_app/question_detail.html', context)


@login_required
def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            messages.success(request, 'Your question has been posted!')
            return redirect('question_detail', question_id=question.id)
    else:
        form = QuestionForm()

    context = {'form': form}
    return render(request, 'community_app/ask_question.html', context)


@login_required
def profile(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user

    profile_obj, created = UserProfile.objects.get_or_create(user=user)
    questions = Question.objects.filter(user=user).order_by('-created_at')
    answers = Answer.objects.filter(user=user).order_by('-created_at')
    journeys = Journey.objects.filter(user=user).order_by('-date')

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile_obj)

    context = {
        'profile_user': user,
        'profile': profile_obj,
        'questions': questions,
        'answers': answers,
        'journeys': journeys,
        'form': form,
    }
    return render(request, 'community_app/profile.html', context)


@login_required
def add_journey(request):
    if request.method == 'POST':
        form = JourneyForm(request.POST)
        if form.is_valid():
            journey = form.save(commit=False)
            journey.user = request.user
            journey.save()
            messages.success(request, 'Journey entry added!')
            return redirect('profile')
    else:
        form = JourneyForm()

    context = {'form': form}
    return render(request, 'community_app/add_journey.html', context)


@login_required
def upvote_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.user in question.upvotes.all():
        question.upvotes.remove(request.user)
    else:
        question.upvotes.add(request.user)

    return redirect('question_detail', question_id=question.id)


@login_required
def upvote_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)

    if request.user in answer.upvotes.all():
        answer.upvotes.remove(request.user)
    else:
        answer.upvotes.add(request.user)

    return redirect('question_detail', question_id=answer.question.id)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = UserRegisterForm()

    context = {'form': form}
    return render(request, 'community_app/register.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'community_app/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')