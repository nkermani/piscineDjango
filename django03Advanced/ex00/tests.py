from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Article, UserFavouriteArticle

class AccessControlTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.article = Article.objects.create(
            title='Test Article',
            author=self.user,
            synopsis='Test Synopsis',
            content='Test Content'
        )

    def test_favourites_view_requires_login(self):
        response = self.client.get(reverse('favourites'))
        self.assertNotEqual(response.status_code, 200)
        # Should redirect to login
        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('favourites'))
        self.assertEqual(response.status_code, 200)

    def test_publications_view_requires_login(self):
        response = self.client.get(reverse('publications'))
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('publications'))
        self.assertEqual(response.status_code, 200)

    def test_publish_view_requires_login(self):
        response = self.client.get(reverse('publish'))
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('publish'))
        self.assertEqual(response.status_code, 200)

    def test_register_view_redirects_authenticated_user(self):
        # Unauthenticated user can access register
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

        # Authenticated user should be redirected
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('register'))
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)

    def test_user_cannot_favourite_article_twice(self):
        self.client.login(username='testuser', password='password')

        # First add
        response = self.client.post(reverse('favourite_create'), {'article': self.article.pk})
        # Should redirect to favourites on success
        self.assertEqual(response.status_code, 302)
        self.assertEqual(UserFavouriteArticle.objects.count(), 1)

        # Second add (try to duplicate)
        response = self.client.post(reverse('favourite_create'), {'article': self.article.pk})
        # Should redirect (handled by try/except IntegrityError)
        self.assertEqual(response.status_code, 302)

        # Count should still be 1
        self.assertEqual(UserFavouriteArticle.objects.count(), 1)
