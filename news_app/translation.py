from modeltranslation import translator
from modeltranslation.translator import register,TranslationOptions

from news_app.models import News, Category


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title','body',)

# translator.register(News, NewsTranslationOptions)
@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)