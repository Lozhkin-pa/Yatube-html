from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django import forms
from ..forms import PostForm
from ..models import Group, Post, Follow
from django.core.cache import cache


User = get_user_model()


class PostsPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test-auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.second_group = Group.objects.create(
            title='Тестовая группа #2',
            slug='second_test-slug',
            description='Тестовое описание #2',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Тестовый пост',
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = self.post.author
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names_for_guest = {
            (reverse('posts:index')): 'posts/index.html',
            (reverse(
                'posts:group_list', kwargs={'slug': self.group.slug}
            )): 'posts/group_list.html',
            (reverse(
                'posts:profile', kwargs={'username': self.post.author}
            )): 'posts/profile.html',
            (reverse(
                'posts:post_detail', kwargs={'post_id': self.post.pk}
            )): 'posts/post_detail.html',
        }
        templates_pages_names_for_auth = {
            (reverse('posts:post_create')): 'posts/create_post.html',
            (reverse(
                'posts:post_edit', kwargs={'post_id': self.post.pk}
            )): 'posts/create_post.html',
            (reverse('posts:follow_index')): 'posts/follow.html',
        }
        for reverse_name, template in templates_pages_names_for_guest.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
        for reverse_name, template in templates_pages_names_for_auth.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertIn('page_obj', response.context)
        first_object = response.context['page_obj'][0]
        post_text_0 = first_object.text
        post_author_0 = first_object.author
        post_group_0 = first_object.group
        post_image_0 = first_object.image
        self.assertEqual(post_text_0, self.post.text)
        self.assertEqual(post_author_0, self.post.author)
        self.assertEqual(post_group_0, self.post.group)
        self.assertEqual(first_object, self.post)
        self.assertNotEqual(post_group_0, self.second_group)
        self.assertEqual(post_image_0, self.post.image)

    def test_group_list_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug})
        )
        self.assertIn('page_obj', response.context)
        first_object = response.context['page_obj'][0]
        post_text_0 = first_object.text
        post_author_0 = first_object.author
        post_group_0 = first_object.group
        post_title_0 = first_object.group.title
        post_slug_0 = first_object.group.slug
        post_image_0 = first_object.image
        self.assertEqual(post_text_0, self.post.text)
        self.assertEqual(post_author_0, self.post.author)
        self.assertEqual(post_title_0, self.post.group.title)
        self.assertEqual(post_slug_0, self.post.group.slug)
        self.assertEqual(first_object, self.post)
        self.assertNotEqual(post_group_0, self.second_group)
        self.assertEqual(post_image_0, self.post.image)

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.post.author})
        )
        self.assertIn('page_obj', response.context)
        first_object = response.context['page_obj'][0]
        post_text_0 = first_object.text
        post_author_0 = first_object.author
        post_group_0 = first_object.group
        post_title_0 = first_object.group.title
        post_slug_0 = first_object.group.slug
        post_image_0 = first_object.image
        self.assertEqual(post_text_0, self.post.text)
        self.assertEqual(post_author_0, self.post.author)
        self.assertEqual(post_title_0, self.post.group.title)
        self.assertEqual(post_slug_0, self.post.group.slug)
        self.assertEqual(first_object, self.post)
        self.assertNotEqual(post_group_0, self.second_group)
        self.assertEqual(post_image_0, self.post.image)

    def test_post_detail_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.pk})
        )
        self.assertIn('one_post', response.context)
        first_object = response.context['one_post']
        post_text_0 = first_object.text
        post_author_0 = first_object.author
        post_title_0 = first_object.group.title
        post_slug_0 = first_object.group.slug
        post_image_0 = first_object.image
        self.assertEqual(post_text_0, self.post.text)
        self.assertEqual(post_author_0, self.post.author)
        self.assertEqual(post_title_0, self.post.group.title)
        self.assertEqual(post_slug_0, self.post.group.slug)
        self.assertEqual(post_image_0, self.post.image)

    def test_post_create_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_create')
        )
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context.get('form'), PostForm)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_post_edit_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk})
        )
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context.get('form'), PostForm)
        form = response.context.get('form')
        self.assertEqual(form.instance, self.post)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_index_page_cached(self):
        """Проверка работы кеша страницы index."""
        first_response = self.authorized_client.get(reverse('posts:index'))
        Post.objects.all().delete()
        second_response = self.authorized_client.get(reverse('posts:index'))
        cache.clear()
        third_response = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(first_response.content, second_response.content)
        self.assertNotEqual(first_response.content, third_response.content)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test-auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        Post.objects.bulk_create([Post(
            author=cls.user,
            group=cls.group,
            text=f'Тестовый пост #{i}',
        ) for i in range(13)]
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_contains_correct_records(self):
        NUM_POSTS_FIRST_PAGE: int = 10
        NUM_POSTS_SECOND_PAGE: int = 3
        rev_page = [
            reverse('posts:index'),
            reverse(
                'posts:group_list', kwargs={'slug': self.group.slug}
            ),
            reverse(
                'posts:profile', kwargs={'username': PaginatorViewsTest.user}
            ),
        ]
        for page in rev_page:
            with self.subTest(page=page):
                response = self.authorized_client.get(page)
                self.assertEqual(
                    len(response.context['page_obj']), NUM_POSTS_FIRST_PAGE
                )
                response = self.authorized_client.get(page + '?page=2')
                self.assertEqual(
                    len(response.context['page_obj']), NUM_POSTS_SECOND_PAGE
                )


class FollowPageTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем автора постов, на которого хотим подписаться
        cls.author_client = Client()
        cls.user_author = User.objects.create(username='author')
        cls.author_client.force_login(cls.user_author)
        # Создаем юзера, которым хотим подписаться на автора (подписчика)
        cls.follower_client = Client()
        cls.user_follower = User.objects.create(username='follower')
        cls.follower_client.force_login(cls.user_follower)
        # Создаем юзера, которым не будем подписываться на автора
        cls.authorized_client = Client()
        cls.user_not_follower = User.objects.create(username='not-follower')
        cls.authorized_client.force_login(cls.user_not_follower)
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user_author,
            group=cls.group,
            text='Тестовый пост',
        )
        cls.post_02 = Post.objects.create(
            author=cls.user_follower,
            group=cls.group,
            text='Пост для тестирования авторизованного пользователя',
        )

    def test_follow_page(self):
        """Шаблон follow сформирован с правильным контекстом."""
        # Подписываемся юзером на автора
        Follow.objects.create(
            user=self.user_follower,
            author=self.user_author
        )
        response = self.follower_client.get(reverse('posts:follow_index'))
        self.assertIn('page_obj', response.context)
        first_object = response.context['page_obj'][0]
        self.assertEqual(first_object, self.post)
        post_text_0 = first_object.text
        post_author_0 = first_object.author
        post_group_0 = first_object.group
        self.assertEqual(post_text_0, self.post.text)
        self.assertEqual(post_author_0, self.post.author)
        self.assertEqual(post_group_0, self.post.group)

    def test_profile_follow_and_unfollow(self):
        """Пользователь может подписываться и отписываться от авторов."""
        first_response = self.follower_client.get(
            reverse('posts:follow_index')
        )
        self.follower_client.post(
            reverse(
                'posts:profile_follow', kwargs={'username': self.user_author}
            )
        )
        second_response = self.follower_client.get(
            reverse('posts:follow_index')
        )
        self.assertNotEqual(first_response.content, second_response.content)
        self.assertTrue(
            Follow.objects.filter(
                user=self.user_follower,
                author=self.user_author,
            ).exists()
        )
        self.follower_client.post(
            reverse(
                'posts:profile_unfollow', kwargs={'username': self.user_author}
            )
        )
        third_response = self.follower_client.get(
            reverse('posts:follow_index')
        )
        self.assertEqual(first_response.content, third_response.content)
        self.assertFalse(
            Follow.objects.filter(
                user=self.user_follower,
                author=self.user_author,
            ).exists()
        )

    def test_new_post_author_on_follow_page(self):
        """Новая запись автора появляется только в ленте подписчика."""
        Follow.objects.create(
            user=self.user_follower,
            author=self.user_author
        )
        Follow.objects.create(
            user=self.user_not_follower,
            author=self.user_follower
        )
        first_follower_response = self.follower_client.get(
            reverse('posts:follow_index')
        )
        follower_client_obj = first_follower_response.context['page_obj'][0]
        self.assertEqual(follower_client_obj.text, self.post.text)
        first_auth_response = self.authorized_client.get(
            reverse('posts:follow_index')
        )
        authorized_client_obj = first_auth_response.context['page_obj'][0]
        self.assertEqual(authorized_client_obj.text, self.post_02.text)
        new_post = Post.objects.create(
            author=self.user_author,
            group=self.group,
            text='Новый пост',
        )
        second_follower_response = self.follower_client.get(
            reverse('posts:follow_index')
        )
        follower_client_obj = second_follower_response.context['page_obj'][0]
        self.assertEqual(follower_client_obj.text, new_post.text)
        second_auth_response = self.authorized_client.get(
            reverse('posts:follow_index')
        )
        authorized_client_obj = second_auth_response.context['page_obj'][0]
        self.assertNotEqual(authorized_client_obj.text, new_post.text)
        self.assertEqual(authorized_client_obj.text, self.post_02.text)
