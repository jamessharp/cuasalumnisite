from cuasalumnisite.news.models import Article
from cuasalumnisite import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

def articleList(request):
    # Get the article list ordered newest to oldest
    article_list = Article.objects.order_by("-time")
    
    #Get a 10 item paginator
    paginator = Paginator(article_list, settings.NEWS_ARTICLES_PER_PAGE)
    
    # Get the page request
    page = request.GET.get("page")
    try:
        articles = paginator.page(page)
    except EmptyPage:
        # if we get an empty page then we've gone too far - give the last page
        articles = paginator.page(paginator.num_pages)
    except:
        # Just give first page if we're not an integer
        articles = paginator.page(1)
        
    return render_to_response("news/article_list.html", 
                              {"article_list": articles},
                              context_instance=RequestContext(request))
    
def articleDetail(request, article_id):
    
    article = get_object_or_404(Article, pk=article_id)
    
    return render_to_response("news/article_detail.html",
                              {"article" : article},
                              context_instance=RequestContext(request))
    
        