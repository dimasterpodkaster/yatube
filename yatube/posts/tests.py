import tempfile

from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from .models import Post, Group, Comment, Follow
from . import views
from django.urls import reverse
from django.core.cache import cache
from django.test import override_settings

User = get_user_model()


class TestStringMethods(TestCase):
    def test_length(self):
        self.assertEqual(len('yatube'), 6)


class ProfileTest(TestCase):
    def setUp(self):
        # создание тестового клиента — подходящая задача для функции setUp()
        self.client = Client()
        # создаём пользователя
        self.user = User.objects.create_user(
            username="sarah", email="connor.s@skynet.com", password="12345"
        )
        # создаём пост от имени пользователя
        self.post = Post.objects.create(
            text="You're talking about things I haven't done yet in the past tense. It's driving me crazy!",
            author=self.user)
        self.group = Group.objects.create(
            title="Burgers",
            slug="burgers",
            description="This is a group about burgers"
        )

    def test_profile(self):
        # формируем GET-запрос к странице сайта
        response = self.client.get("/sarah/")
        # проверяем что страница найдена
        self.assertEqual(response.status_code, 200)

    def test_accessing_post_page(self):
        # Авторизируем пользователя
        self.client.login(username='sarah', password='12345')
        # формируем GET-запрос к странице сайта
        response = self.client.get("/new/")
        # проверяем что страница найдена
        self.assertEqual(response.status_code, 200)

    def test_redirecting_post_page(self):
        # Выйдем из аккаунта пользователя
        self.client.logout()
        # формируем GET-запрос к странице сайта
        response = self.client.get("/new/")
        # проверяем что страница найдена
        self.assertEqual(response.status_code, 302)

    def test_post_addition(self):
        response = self.client.get("")
        self.assertEqual(response.context["page"][0], self.post)
        response = self.client.get("/sarah/")
        self.assertEqual(len(response.context["page"]), 1)
        self.client.login(username='sarah', password='12345')
        id_for_post = self.post.pk
        message = "/sarah/" + str(id_for_post)
        response = self.client.get(message, follow=True)
        self.assertEqual(response.context["posts"][0], self.post)

    def test_post_editing(self):
        self.client.login(username='sarah', password='12345')
        self.client.get(f'/{self.user.username}/{self.post.pk}/edit/')
        self.post_id = self.post.pk
        response = self.client.post(reverse('post_edit', kwargs={
            'username': self.user.username,
            'post_id': self.post_id}),
                                    data={'text': 'Changed text',
                                          'group': self.group.id},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.get(id=self.post.pk).text, 'Changed text')


class TestExceptionErrors(TestCase):
    def setUp(self):
        # создание тестового клиента — подходящая задача для функции setUp()
        self.client = Client()

    def test_404(self):
        response = self.client.get("/123/")
        self.assertEqual(response.status_code, 404)


class TestPhotosUpdate(TestCase):
    def setUp(self):
        self.client = Client()
        # создаём пользователя
        self.user = User.objects.create_user(
            username="sarah", email="connor.s@skynet.com", password="12345"
        )
        self.client.force_login(self.user)

    def test_tag(self):
        # cache.clear()
        with tempfile.TemporaryDirectory() as temp_directory:
            with override_settings(MEDIA_ROOT=temp_directory):
                with open('/Users/dmitriinizovcev/Dev/hw04_tests-master/media/posts/IMG_0737.png', 'rb') as img:
                    post = self.client.post(reverse("new_post"),
                                            {'author': self.user, 'text': 'post with image', 'image': img}, follow=True)

        self.assertEqual(post.status_code, 200)
        self.assertEqual(Post.objects.count(), 1)

        post = Post.objects.first()

        self.urls = {
            reverse('index'),
            reverse('post', kwargs={"username": self.user.username, "post_id": post.pk}),
            reverse('profile', kwargs={"username": self.user.username})
        }

        for url in self.urls:
            cache.clear()
            response = self.client.get(url)
            self.assertContains(response, 'unique_id')

        with open('/Users/dmitriinizovcev/Documents/Monologue.pages', 'rb') as text_file:
            post = self.client.post(reverse("new_post"),
                                    {'author': self.user, 'text': 'post with image', 'image': text_file}, follow=True)

        self.assertEqual(Post.objects.count(), 1)

        with tempfile.TemporaryDirectory() as temp_directory:
            with override_settings(MEDIA_ROOT=temp_directory):
                with open('/Users/dmitriinizovcev/Dev/hw04_tests-master/media/posts/IMG_0737.png', 'rb') as img:
                    post = self.client.post(reverse("new_post"),
                                            {'author': self.user, 'text': 'post with image', 'image': img}, follow=True)

        response = self.client.get(reverse('index'))
        self.assertEqual(len(response.context["page"]), 2)


class TestFollow(TestCase):
    def setUp(self):
        self.client_1 = Client()
        # создаём пользователя
        self.user1 = User.objects.create_user(
            username="Sarah", email="connor.s@skynet.com", password="12345"
        )
        self.post1 = Post.objects.create(
            text="You're talking about things crazy!",
            author=self.user1)
        self.client_2 = Client()
        # создаём пользователя
        self.user2 = User.objects.create_user(
            username="Andrew", email="andrewgarfield@skynet.com", password="789123"
        )
        self.post2 = Post.objects.create(
            text="You're talking about things I haven't done yet in the past tense. It's driving me crazy!",
            author=self.user2)
        self.client_3 = Client()
        # создаём пользователя
        self.user3 = User.objects.create_user(
            username="Antonio", email="Anto_ba@skynet.com", password="123456789"
        )

    def test_subscribing(self):
        self.client_1.force_login(self.user1)
        response = self.client_1.get(f'/{self.user2.username}/follow/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Follow.objects.count(), 1)

    def test_subscription(self):
        self.client_1.force_login(self.user1)
        self.client_1.get(f'/{self.user2.username}/follow/', follow=True)
        response = self.client_1.get(reverse("follow_index"), follow=True)
        self.assertEqual(len(response.context["page"]), 1)
        self.client_2.force_login(self.user2)
        response = self.client_2.get(reverse("follow_index"), follow=True)
        self.assertEqual(len(response.context["page"]), 0)

    def test_comments(self):
        comment = self.client_1.post(reverse("add_comment",
                                             kwargs={"username": self.user1.username, "post_id": self.post1.pk}),
                                     {'text': 'post with image'}, follow=True)
        self.assertEqual(Comment.objects.count(), 0)
        self.client_1.force_login(self.user1)
        comment = self.client_1.post(reverse("add_comment",
                                             kwargs={"username": self.user1.username, "post_id": self.post1.pk}),
                                     {'text': 'post with image'}, follow=True)
        self.assertEqual(Comment.objects.count(), 1)
