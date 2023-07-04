from django.urls import reverse
from rest_framework.test import APITestCase
import json
from rest_framework import status


class EntriesTestCase(APITestCase):
    # post
    def test_post_correct_data(self): 
        test_data = {"category": "personal_details", "name": "John Doe","Age":"20"}
        response=self.client.post(reverse('entries'),json.dumps(test_data),content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_post_incorrect_data(self):
        # no category key 
        test_data = {"name": "John Doe","Age":"20"}
        response=self.client.post(reverse('entries'),json.dumps(test_data),content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_search_category_with_correct_format(self):
        # we have previously posted category personal_details 
        test_data = {"category": "personal_details"}
        response=self.client.post(reverse('category'),json.dumps(test_data),content_type="application/json")   
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_search_category_with_incorrect_format(self):
        # the category key should be passed in the post request. This should return an error
        test_data = {"unknown_key": "personal_details"}
        response=self.client.post(reverse('category'),json.dumps(test_data),content_type="application/json")   
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
                
    def test_search_existing_field_with_keywords(self):
        '''
        the format for searching is 
        {
           "keywords": "kw_1, kw_2",
          "field":"field_to_search"
          }
            
        '''
        test_data = {"keywords": "john","field":"name"}
        response=self.client.post(reverse('search'),json.dumps(test_data),content_type="application/json")   
        self.assertEqual(response.status_code, status.HTTP_200_OK)
                
# get all
# find category
# search
