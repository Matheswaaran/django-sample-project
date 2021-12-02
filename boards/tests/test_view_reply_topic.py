from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve

from ..forms import PostForm
from ..models import Board, Topic, Post
from ..views import reply_topic


class ReplyToTopicTestCase(TestCase):
    """
    Base test class for the Reply to topic test case
    """

    def setUp(self):
        self.board = Board.objects.create(name='Django', description="Django Board.")
        self.username = 'john'
        self.password = '123'
        self.email = 'mat@mat.com'
        user = User.objects.create_user(username=self.username, email=self.email, password=self.password)
        self.topic = Topic.objects.create(subject="Part 1", board=self.board, starter=user)
        self.post = Post.objects.create(message='Lorem ipsum dolor sit amet', topic=self.topic, created_by=user)
        self.url = reverse('reply_topic', kwargs={'board_id': self.board.pk, 'topic_pk': self.topic.pk})


class LoginRequiredReplyTopicTests(ReplyToTopicTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))


class ReplyTopicsTest(ReplyToTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/boards/1/topics/1/reply/')
        self.assertEquals(view.func, reply_topic)

    def test_csrf_token_for_reply_form(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PostForm)

    def test_reply_from_inputs(self):
        """
        The view must have two inputs: csrf, message: textarea
        """
        self.assertContains(self.response, '<input', 1)
        self.assertContains(self.response, '<textarea', 1)


class SuccessfulFormSubmitToReplyTopics(ReplyToTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {'message': 'Hello world'})

    def test_redirection(self):
        """
        A valid form submission should redirect the user to topics page
        """
        topic_posts_url = reverse('topic_posts', kwargs={'board_id': self.board.pk, 'topic_pk': self.topic.pk})
        self.assertRedirects(self.response, topic_posts_url)

    def test_new_reply_created(self):
        """
        The total post count should be 2
        The one created in the `ReplyToTopicTestCase` setUp
        and another created by the post data in this class
        """
        self.assertEquals(Post.objects.count(), 2)


class InvalidFormSubmitToReplyTopics(ReplyToTopicTestCase):
    def setUp(self):
        """
        Submit an empty dictionary to the view
        """
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        """
        An invalid form submission should return the same page
        """
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)