from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from ..models import Group, Post
from http import HTTPStatus

User = get_user_model()


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test-auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = self.post.author
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages(self):
        """Доступность вызываемой страницы."""
        page_list_for_guest_client = [
            '/',
            f'/group/{self.group.slug}/',
            f'/profile/{self.post.author}/',
            f'/posts/{self.post.pk}/'
        ]
        page_list_for_authorized_client = [
            '/create/',
            f'/posts/{self.post.pk}/edit/',
            '/follow/',
        ]
        for page in page_list_for_guest_client:
            with self.subTest(page=page):
                response = self.guest_client.get(page)
                self.assertEqual(response.status_code, HTTPStatus.OK)
        for page in page_list_for_authorized_client:
            with self.subTest(page=page):
                response = self.authorized_client.get(page)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_unexpecting_page(self):
        """Запрос к несуществующей странице вернёт ошибку."""
        response = self.guest_client.get('/unexpecting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names_for_guest_client = {
            'posts/index.html': '/',
            'posts/group_list.html': f'/group/{self.group.slug}/',
            'posts/profile.html': f'/profile/{self.post.author}/',
            'posts/post_detail.html': f'/posts/{self.post.pk}/',
            'core/404.html': '/unexpecting_page/',
        }
        templates_url_names_for_auth_client = {
            '/create/': 'posts/create_post.html',
            f'/posts/{self.post.pk}/edit/': 'posts/create_post.html',
            '/follow/': 'posts/follow.html',
        }
        for template, address in templates_url_names_for_guest_client.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)
        for address, template in templates_url_names_for_auth_client.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
