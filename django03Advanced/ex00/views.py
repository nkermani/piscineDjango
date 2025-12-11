from django.views.generic import ListView, RedirectView, DetailView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db import IntegrityError, transaction
from .models import Article, UserFavouriteArticle
from .forms import PublishForm, FavouriteForm

class ArticleListView(ListView):
    model = Article
    template_name = 'ex00/articles.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.select_related('author').defer('content').order_by('-created')

class HomeView(RedirectView):
    url = reverse_lazy('articles')

class CustomLoginView(LoginView):
    template_name = 'ex00/login.html'

    def get_success_url(self):
        return reverse_lazy('home')

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'ex00/detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favourite_form'] = FavouriteForm(initial={'article': self.object})
        return context

class PublicationListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'ex00/publications.html'
    context_object_name = 'publications'

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user).values('pk', 'title', 'created', 'synopsis')

class FavouriteListView(LoginRequiredMixin, ListView):
    model = UserFavouriteArticle
    template_name = 'ex00/favourites.html'
    context_object_name = 'favourites'

    def get_queryset(self):
        return UserFavouriteArticle.objects.filter(user=self.request.user).select_related('article')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'ex00/register.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class PublishArticleView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = PublishForm
    template_name = 'ex00/publish.html'
    success_url = reverse_lazy('publications')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class FavouriteCreateView(LoginRequiredMixin, CreateView):
    model = UserFavouriteArticle
    form_class = FavouriteForm
    success_url = reverse_lazy('favourites')

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            with transaction.atomic():
                return super().form_valid(form)
        except IntegrityError:
            return redirect('favourites')
