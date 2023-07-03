import json
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from pymongo import MongoClient
from rest_framework.response import Response
from bson.json_util import dumps,loads
from api.serializers import DataSerializer
# connection string
connection_string='mongodb://localhost:27017'
client=MongoClient(connection_string)

# get database
db_instance=client.get_database('demo_database')
# create collections dynamically 
# check whether collection exists and if so, add the data to the existing collection

def getDB(request):
    # return HttpResponse(db_instance.collection_names())
    import datetime
    post = {
        "author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.now(tz=datetime.timezone.utc),
        "mydate": datetime.datetime.now(tz=datetime.timezone.utc),
        "secondat": datetime.datetime.now(tz=datetime.timezone.utc),
     
        }
    posts = db_instance.posts
    post_id = posts.insert_one(post).inserted_id
    return HttpResponse(post_id)

# class Add(APIView):
    
#     def get(self, request, *args, **kwargs):
#         if "posts" in db_instance.list_collection_names():   
#            return HttpResponse('exists')
              
#         else:
#            return HttpResponse('doesnt exist')
@api_view(['GET', 'POST'])
def add(request, *args, **kwargs):
    if request.method == 'POST':
        post = json.loads(request.body)
       
        if "category" in post:
            db_instance.posts.insert_one(post)
            return HttpResponse('Data saved')
            
        else:
            return HttpResponse('Category key reqired')
            
    # check whether the passed document has a category field*
    # if not, return an error
    # this category feld will be used during search
    
    # find -> search/sort based on category
    # only unique items should be saved
    # urls: add a field/must pass its category in json -> post request
    # view category
    # view records via search
    
class Search(APIView):
    def get(self,request, category):
        category_data= db_instance.posts.find( { "category": category})
        serializer = DataSerializer(category_data, many=True)
        return JsonResponse(serializer.data,safe=False)