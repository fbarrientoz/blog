from django.contrib.auth import  get_user_model
from django.test import  TestCase
from django.urls import reverse

from .models import Post

class BlogTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='user',email='mail.conm', password='...'
        )

        self.post = Post.objects.create(
            title="title",body='nice body', author=self.user
        )

    def test_string_representation(self):
        post = Post(title='title')
        self.assertEqual(str(post), post.title)

    
    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), '/post/1/')


    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'title')
        self.assertEqual(f'{self.post.author}', 'user')
        self.assertEqual(f'{self.post.body}', 'nice body')


    def test_post_list_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "title")
        self.assertTemplateUsed(response, "post_detail.html")


    def test_post_create_view(self):
        response = self.client.post(reverse('post_new'), {
            'title':'New title',
            'body':'New text',
            'author':self.user.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, "New title")
        self.assertEqual(Post.objects.last().body, "New text")

    def test_post_update_view(self):
        response = self.client.post(reverse('post_edit', args='1'), {
            
            'title':'Update title',
            'body':'Updated text',
        })
        self.assertEqual(response.status_code, 200)


    def test_post_delete_view(self):
        response = self.client.post(reverse('post_delete', args='1'), {
            
            'title':'Update title',
            'body':'Updated text',
        })
        self.assertEqual(response.status_code, 302) # 302 successfull redirection
