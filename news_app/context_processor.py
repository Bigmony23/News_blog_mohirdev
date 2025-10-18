from .models import News, Category


def latest_news(request):
    category_news = Category.objects.all()
    latest_news = News.published.all().order_by('-publish_time')[:10]
    context = {"latest_news": latest_news, "category_news": category_news}
    return context
