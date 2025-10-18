from lib2to3.fixes.fix_input import context

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView

from .models import News,Category
from .forms import ContactForm

def news_list(request):
    news_all = News.objects.filter()
    news_all=News.published.all()
    context = {'news_all':news_all}

    return render(request,"news/news_list.html", context=context)

def news_detail(request,news):
    news = get_object_or_404(News,slug=news)
    context = {'news':news}
    return render(request,'news/news_detail.html',context)

def homeView(request):
    news = News.published.all().order_by('-publish_time')[:5]
    categories = Category.objects.all()
    local_one= News.published.filter(category__name="Local").order_by('-publish_time')[:1]
    local_news = News.published.all().filter(category__name="Local").order_by('-publish_time')[1:6]
    context = {
        'news':news,
        'categories':categories,
        "local_news":local_news,
        "local_one":local_one
    }
    return render(request,'news/index.html',context)

# def ContactView(request):
#     form = ContactForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         form.save()
#         return HttpResponse('Your message has been sent.')
#     context = {'form':form}
#     return render(request,'news/contact.html',context)


class HomePageView(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['categories']=Category.objects.all()
        context['news']=News.published.all().order_by('-publish_time')[:5]
        # context['local_one']=News.published.filter(category__name="Local").order_by('-publish_time')[:1]
        context['local_news']=News.published.filter(category__name="Local").order_by('-publish_time')[:5]
        context['world_news'] = News.published.filter(category__name="World").order_by('-publish_time')[:5]
        context['tecno_news'] = News.published.filter(category__name="Technologia").order_by('-publish_time')[:5]
        context['sport_news'] = News.published.filter(category__name="Sport").order_by('-publish_time')[:5]
        return context

class ContactView(TemplateView):
    template_name = 'news/contact.html'

    def get(self,request,*args, **kwargs):
        form = ContactForm()
        context={'form':form}
        return render(request,'news/contact.html',context)

    def post(self,request,*args,**kwargs):

        form = ContactForm(request.POST)
        if  request.method=='POST' and form.is_valid():
            form.save()
            return HttpResponse('Your message has been sent.')
        context = {'form':form}
        return render(request,'news/contact.html',context)

class AboutView(TemplateView):
    template_name = 'news/about_us.html'

class LocalNewsView(ListView):
    model = News
    template_name = 'news/local_news.html'
    context_object_name = 'local_news'

    def get_queryset(self):
        news=News.published.all().filter(category__name="Local")
        return news




class SportNewsView(ListView):
    model = News
    template_name = 'news/sport_news.html'
    context_object_name = 'sport_news'

    def get_queryset(self):
        news=News.published.all().filter(category__name="Sport")
        return news


class TecnologyNewsView(ListView):
    model = News
    template_name = 'news/tecno_news.html'
    context_object_name ='tecno_news'

    def get_queryset(self):
        news=News.published.all().filter(category__name="Technologia")
        return news

class WorldNewsView(ListView):
    model = News
    template_name = 'news/world_news.html'
    context_object_name = 'world_news'

    def get_queryset(self):
        news=News.published.all().filter(category__name="World")
        return news
# Create your views here.
