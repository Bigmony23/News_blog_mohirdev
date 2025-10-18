from django.urls import path


from .views import news_list, news_detail, homeView, ContactView, AboutView,HomePageView,LocalNewsView,SportNewsView,WorldNewsView,TecnologyNewsView

urlpatterns=[
    path('',HomePageView.as_view(),name='home_page'),
    path('all-news/', news_list, name='news_list'),
    path('news<slug:news>/', news_detail, name='news_detail'),
    path('contact/',ContactView.as_view(), name='contact'),
    path('about/',AboutView.as_view(), name='about'),
    path('sport/',SportNewsView.as_view(), name='sport_news'),
    path('world/',WorldNewsView.as_view(), name='world_news'),
    path('local/',LocalNewsView.as_view(), name='local_news'),
    path('tecnology/',TecnologyNewsView.as_view(), name='tecno_news'),
]

