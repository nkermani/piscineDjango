from django.urls import path
from .views import ArticleListView, HomeView, CustomLoginView, ArticleDetailView, PublicationListView, FavouriteListView, CustomLogoutView, RegisterView, PublishArticleView, FavouriteCreateView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('articles/', ArticleListView.as_view(), name='articles'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('detail/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('publications/', PublicationListView.as_view(), name='publications'),
    path('favourites/', FavouriteListView.as_view(), name='favourites'),
    path('register/', RegisterView.as_view(), name='register'),
    path('publish/', PublishArticleView.as_view(), name='publish'),
    path('favourite/', FavouriteCreateView.as_view(), name='favourite_create'),
]
