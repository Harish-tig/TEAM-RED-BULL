from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Question, Answer, Journey, UserProfile, Category


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'health_interest', 'expertise', 'profile_picture']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'description', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }


class JourneyForm(forms.ModelForm):
    class Meta:
        model = Journey
        fields = ['title', 'symptom', 'test', 'doctor', 'treatment', 'notes', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'symptom': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


from django import forms
from .models import Question, Answer, Journey, UserProfile, Category


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'description', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Be specific about your health concern'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control form-textarea',
                'placeholder': 'Include details like: symptoms, duration, what you\'ve tried, doctor visits...',
                'rows': 6
            }),
            'category': forms.Select(attrs={
                'class': 'form-control form-select'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make fields required
        self.fields['title'].required = True
        self.fields['description'].required = True
        self.fields['category'].required = False