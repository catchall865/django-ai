from django.shortcuts import render
from django.contrib import messages
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
                return render(request, 'suggest.html', {'lang_list': lang_list, 'lang': lang, 'response': response})
            except Exception as e:
                return render(request, 'suggest.html', {'lang_list': lang_list, 'response': e, 'lang': lang})



    return render(request, 'suggest.html', {'lang_list': lang_list})