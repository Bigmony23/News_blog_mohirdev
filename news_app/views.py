from audioop import reverse
from lib2to3.fixes.fix_input import context

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView,CreateView
from hitcount.templatetags.hitcount_tags import get_hit_count
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin

from .models import News,Category
from .forms import ContactForm, CommentForm
from .custom_permissions import OnlyLoggedUsers
def news_list(request):
    news_all = News.objects.filter()
    news_all=News.published.all()
    context = {'news_all':news_all}

    return render(request,"news/news_list.html", context=context)

def news_detail(request,news):
    news = get_object_or_404(News,slug=news)
    context = {}
    #hitcount
    hit_count=get_hitcount_model().objects.get_for_object(news)
    hits=hit_count.hits
    hit_context=context["hit_count"]={'pk':hit_count.pk}
    hitcount_response=HitCountMixin.hit_count(request,hit_count)
    if hitcount_response.hit_counted:
        hits=hits+1
        hit_context['hit_counted']=hitcount_response.hit_counted
        hit_context['hit_message']=hitcount_response.hit_message
        hit_context['total_hits']=hits
    
    comments = news.comments.filter(active=True)
    comments_count=comments.count()
    new_comments=None
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comments = comment_form.save(commit=False)
            new_comments.news = news
            new_comments.user = request.user
            new_comments.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    context = {'news':news,'comments':comments,"new_comments":new_comments,'comment_form':comment_form,'comments_count':comments_count}
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

class NewsUpdateView(OnlyLoggedUsers,UpdateView):
    model = News
    fields = ('title','body','image','category','status')
    template_name = 'crud/news_edit.html'

class NewsDeleteView(OnlyLoggedUsers,DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')

class NewsCreateView(OnlyLoggedUsers,CreateView):
    model = News
    fields = ('title','slug','body','image','category','status')
    template_name = 'crud/news_create.html'
@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_page(request):
    admin_user = User.objects.filter(is_superuser=True )

    context = {
        'admin_user':admin_user
    }
    return render(request,'pages/admin_page.html',context)

class SearchResultList(ListView):
    model = News
    template_name = 'news/search.html'
    context_object_name = 'search_news'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(Q(title__icontains=query) | Q(body__icontains=query)

        )



