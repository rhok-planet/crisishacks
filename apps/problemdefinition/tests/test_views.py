from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from grid.models import Element, Feature, GridHack

class FunctionalGridTest(TestCase):
    fixtures = ['test_initial_data.json']
    
    def test_grid_list_view(self):
        client = Client()
        url = reverse('grids')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'grid/grids.html')
        
    def test_grid_detail_view(self):
        client = Client()
        url = reverse('grid', kwargs={'slug': 'testing'})
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'grid/grid_detail.html')
    
    def test_add_grid_view(self):
        client = Client()
        url = reverse('add_grid')
        response = client.get(url)
        
        # The response should be a redirect, since the user is not logged in.
        self.assertEqual(response.status_code, 302)
        
        # Once we log in the user, we should get back the appropriate response.
        self.assertTrue(client.login(username='user', password='user'))
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'grid/add_grid.html')
    
    def test_edit_grid_view(self):
        client = Client()
        url = reverse('edit_grid', kwargs={'slug': 'testing'})
        response = client.get(url)
        
        # The response should be a redirect, since the user is not logged in.
        self.assertEqual(response.status_code, 302)
        
        # Once we log in the user, we should get back the appropriate response.
        self.assertTrue(client.login(username='user', password='user'))
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'grid/edit_grid.html')
    
    def test_add_feature_view(self):
        client = Client()
        url = reverse('add_feature', kwargs={'grid_slug': 'testing'})
        response = client.get(url)
        
        # The response should be a redirect, since the user is not logged in.
        self.assertEqual(response.status_code, 302)
        
        # Once we log in the user, we should get back the appropriate response.
        self.assertTrue(client.login(username='user', password='user'))
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'grid/add_feature.html')
        
    def test_edit_feature_view(self):
        client = Client()
        url = reverse('edit_feature', kwargs={'id': '1'})
        response = client.get(url)
        
        # The response should be a redirect, since the user is not logged in.
        self.assertEqual(response.status_code, 302)
        
        # Once we log in the user, we should get back the appropriate response.
        self.assertTrue(client.login(username='user', password='user'))
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'grid/edit_feature.html')

    def test_delete_feature_view(self):
        count = Feature.objects.count()
        client = Client()
        
        # Since this user doesn't have the appropriate permissions, none of the
        # features should be deleted (thus the count should be the same).
        self.assertTrue(client.login(username='user', password='user'))
        url = reverse('delete_feature', kwargs={'id': '1'})
        response = client.get(url)
        self.assertEqual(count, Feature.objects.count())
        
        # Once we log in with the appropriate user, the request should delete
        # the given feature, reducing the count by one.
        self.assertTrue(client.login(username='cleaner', password='cleaner'))
        response = client.get(url)
        self.assertEqual(count - 1, Feature.objects.count())

    def test_edit_element_view(self):
        client = Client()
        url = reverse('edit_element', kwargs={'feature_id': '1', 'hack_id': '1'})
        response = client.get(url)
        
        # The response should be a redirect, since the user is not logged in.
        self.assertEqual(response.status_code, 302)
        
        # Once we log in the user, we should get back the appropriate response.
        self.assertTrue(client.login(username='user', password='user'))
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'grid/edit_element.html')

    def test_add_gridhack_view(self):
        client = Client()
        url = reverse('add_grid_hack', kwargs={'grid_slug': 'testing'})
        response = client.get(url)
        
        # The response should be a redirect, since the user is not logged in.
        self.assertEqual(response.status_code, 302)
        
        # Once we log in the user, we should get back the appropriate response.
        self.assertTrue(client.login(username='user', password='user'))
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'grid/add_grid_hack.html')

    def test_delete_gridhack_view(self):
        count = GridHack.objects.count()
        client = Client()
        
        # Since this user doesn't have the appropriate permissions, none of the
        # features should be deleted (thus the count should be the same).
        self.assertTrue(client.login(username='user', password='user'))
        url = reverse('delete_grid_hack', kwargs={'id': '1'})
        response = client.get(url)
        self.assertEqual(count, GridHack.objects.count())
        
        # Once we log in with the appropriate user, the request should delete
        # the given feature, reducing the count by one.
        self.assertTrue(client.login(username='cleaner', password='cleaner'))
        response = client.get(url)
        self.assertEqual(count - 1, GridHack.objects.count())

    def test_latest_grids_view(self):
        client = Client()
        url = reverse('latest_grids')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'grid/grid_archive.html')

class RegressionGridTest(TestCase):
    fixtures = ['test_initial_data.json']
    
    def test_edit_element_view_for_nonexistent_elements(self):
        """Make sure that attempts to edit nonexistent elements succeed.
        
        """
        client = Client()

        # Delete the element for the sepcified feature and hack.        
        element, created = Element.objects.get_or_create(feature=1, grid_hack=1)
        element.delete()
        
        # Log in the test user and attempt to edit the element.
        self.assertTrue(client.login(username='user', password='user'))

        url = reverse('edit_element', kwargs={'feature_id': '1', 'hack_id': '1'})
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'grid/edit_element.html')
            












        