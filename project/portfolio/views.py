from django.shortcuts import render,redirect
from django.views.generic import View
from .forms import ContactForm
from .models import Profile, Work, Experience,Education,Language,Framework
from django.conf import settings
from django.core.mail import BadHeaderError,EmailMessage,send_mail
from django.http import HttpResponse
import textwrap

# Create your views here.


class IndexView(View):
    def get(self, request, *args, **kwargs):
        profile_data = Profile.objects.all()
        if profile_data.exists():
            profile_data = profile_data.order_by('-id')[0]
        work_data = Work.objects.order_by('-id')
        return render(request, 'portfolio/index.html', {
            'profile_data': profile_data,
            'work_data': work_data
        })


class DetailView(View):
    def get(self,request, *args, **kwargs):
        work_data = Work.objects.get(id=self.kwargs['pk'])
        return render(request, 'portfolio/detail.html', {
            'work_data':work_data
        })


class AboutView(View):
    def get(self,request, *args, **kwargs):
        profile_data = Profile.objects.all()
        if profile_data.exists():
            profile_data = profile_data.order_by('-id')[0]
        experience_data = Experience.objects.order_by('-id')
        education_data = Education.objects.order_by('-id')
        language_data = Language.objects.order_by('-id')
        framework_data = Framework.objects.order_by('-id')
        return render(request, 'portfolio/about.html', {
            'profile_data': profile_data,
            'experience_data':experience_data,
            'education_data': education_data,
            'language_data': language_data,
            'framework_data':framework_data
        })


class ContactView(View):
    def get(self,request, *args, **kwargs):
        form = ContactForm(request.POST or None)
        return render(request,'portfolio/contact.html', {
            'form':form
        })

    def post(self,request, *args, **kwargs):
        form = ContactForm(request.POST or None)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            subject = 'お問い合わせありがとうございます。'
            contact = textwrap.dedent('''
                ※このメールはシステムからの自動返信です。

                {name}様

                お問い合わせありがとうございました。
                以下の内容でお問い合わせを受け付けました。
                内容を確認させていただき、ご返信させていただきますので、少々お待ち下さい。

                -------------------------------------
                ■お名前
                {name}

                ■メールアドレス
                {email}

                ■メッセージ
                {message}

                -------------------------------------
            ''').format(
                name=name,
                email=email,
                message=message
            )
            to_list = [email]
            bcc_list = [settings.EMAIL_HOST_USER]

            try:
                message = EmailMessage(subject=subject, body=contact, to=to_list, bcc=bcc_list)
                message.send()
            except BadHeaderError:
                return HttpResponse('無効なヘッダが検出されました。')
                
            return redirect('thanks')

        return render(request,'portfolio/contact.html', {
            'form':form
        })


class ThanksView(View):
    def get(self,request, *args, **kwargs):
        return render(request, 'portfolio/thanks.html')