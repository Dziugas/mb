from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail

from .models import Article
from .forms import ContactForm

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def blog(request):
    articles = Article.objects.all().order_by('-date')
    return render (request, 'blog.html', {'articles': articles})

def article_detail(request, slug):
    article = Article.objects.get(slug = slug)
    return render(request, 'article_detail.html', {'article': article})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            senders_name = form.cleaned_data['name']
            senders_email = form.cleaned_data['email']
            senders_message = form.cleaned_data['message']

            message = "From: %s\n\n" \
                      "Email: %s\n\n" \
                      "Text:\n\n%s"\
                      %(senders_name, senders_email, senders_message)

            from_email = settings.EMAIL_HOST_USER
            to_email = [from_email]
            send_mail('Message from the Mood Balance contact form',
                      message,
                      from_email,
                      to_email,
                      fail_silently=False
                      )
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form':form})


