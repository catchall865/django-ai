from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from .models import Code
import openai
import os

API_KEY = os.environ['API_KEY']

# Create your views here.
def home(request):
    lang_list = ['c', 'clike', 'cpp', 'csharp', 'css', 'dart', 'django', 'go', 'java', 'javascript', 'markup', 'markup-templating', 'perl', 
'php', 'powershell', 'python', 'regex', 'ruby', 'rust', 'sass', 'sql', 'swift', 'yaml']

    if request.method == "POST":
        code = request.POST['code']
        lang = request.POST['lang']

        if lang =='Select Programming Language':
            messages.success(request, 'You did not select a programming language.')
            return render(request, 'home.html', {'lang_list': lang_list, 'code': code, 'lang': lang})
        else:
            openai.api_key = API_KEY
            openai.Model.list()

            try:
                response = openai.Completion.create(
                    model='text-davinci-003',
                    prompt=f'Response only with code. Fix this {lang} code: {code}',
                    temperature=0,
                    max_tokens=1000,
                    top_p=1.0,
                    presence_penalty=0.0,
                    frequency_penalty=0.0
                )
                response = (response['choices'][0]['text']).strip()

                record = Code(question=code, code_answer=response, language=lang, user=request.user)
                record.save()

                return render(request, 'home.html', {'lang_list': lang_list, 'lang': lang, 'response': response})
            except Exception as e:
                return render(request, 'home.html', {'lang_list': lang_list, 'response': e, 'lang': lang})



    return render(request, 'home.html', {'lang_list': lang_list})

def suggest(request):
    lang_list = ['c', 'clike', 'cpp', 'csharp', 'css', 'dart', 'django', 'go', 'java', 'javascript', 'markup', 'markup-templating', 'perl', 
'php', 'powershell', 'python', 'regex', 'ruby', 'rust', 'sass', 'sql', 'swift', 'yaml']

    if request.method == "POST":
        code = request.POST['code']
        lang = request.POST['lang']

        if lang =='Select Programming Language':
            messages.success(request, 'You did not select a programming language.')
            return render(request, 'suggest.html', {'lang_list': lang_list, 'code': code, 'lang': lang})
        else:
            openai.api_key = API_KEY
            openai.Model.list()

            try:
                response = openai.Completion.create(
                    model='text-davinci-003',
                    prompt=f'Response only with code. {code}',
                    temperature=0,
                    max_tokens=1000,
                    top_p=1.0,
                    presence_penalty=0.0,
                    frequency_penalty=0.0
                )
                response = (response['choices'][0]['text']).strip()

                record = Code(question=code, code_answer=response, language=lang, user=request.user)
                record.save()

                return render(request, 'suggest.html', {'lang_list': lang_list, 'lang': lang, 'response': response})
            except Exception as e:
                return render(request, 'suggest.html', {'lang_list': lang_list, 'response': e, 'lang': lang})



    return render(request, 'suggest.html', {'lang_list': lang_list})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request=request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in.")
            return redirect('home')
        else:
            messages.success(request, 'Error logging in. Please try again.')
            return redirect('home')
    else:
        return render(request, 'home.html', {})
    

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have successfully registered a new account.')
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form':form})

def past(request):
    if request.user.is_authenticated:
        code = Code.objects.filter(user_id=request.user.id)
        return render(request, 'past.html', {'code': code})
    else:
        messages.success(request, 'You must be logged in to view this page.')
        return redirect('home')
    
def delete_past(request, Past_id):
    past = Code.objects.get(pk=Past_id)
    past.delete()
    messages.success(request, 'Previous entry deleted.')
    return redirect('past')