from django.test import TestCase
from ..models import Author
from django.urls import reverse

class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_authors = 13
        for author_id in range(number_of_authors):
            Author.objects.create(
                first_name=f'Dminique {author_id}',
                last_name=f'Surname {author_id}',
            )
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/authors/')
        self.assertEqual(response.status_code, 200)
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('catalog:authors'))
        self.assertEqual(response.status_code, 200)
    def test_pagination_is_ten(self):
        response = self.client.get(reverse('catalog:authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['author_list']), 10)
    def test_lists_all_authors(self):
        response = self.client.get(reverse('authors')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['author_list']), 3)