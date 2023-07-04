import json
import re
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from pymongo import MongoClient
from api.serializers import DataSerializer
# connection string
connection_string='mongodb://localhost:27017'
client=MongoClient(connection_string)

# get database
db=client.get_database('demo_database')

class Entries(APIView):
    def get(self,request):
        all_entries= list(db.entries.find())
        if (len(all_entries)) == 0:
            return JsonResponse({'error':'no data'})
        else:
            serializer = DataSerializer(all_entries, many=True)
            return JsonResponse(serializer.data,safe=False)
        
            
    def post(self,request):
        entry = json.loads(request.body)
        # check whether the passed json has only category and data as the top level keys*
        for key in entry.keys():
            if key != 'category' and key !='data':
                return JsonResponse({'error':'data format error'})

        # check if unique
        cursor =list( db.entries.find({"$and": [{"category": entry['category']}, {"data": entry['data']}]}))
        if (len(cursor)) == 0:
            db.entries.insert_one(entry)
            return JsonResponse({'success':'data saved'})
        else:
            return JsonResponse({'error':'data exists'})
            

class Category(APIView):
     # find/search based on category
    def post(self,request, ):
        category = json.loads(request.body)
        # only category field should be passed
        for key in category.keys():
            if key != 'category':
                return JsonResponse({'error':'data format error'})

        category_data= list(db.entries.find( { "category": category['category']}))
        if (len(category_data)) == 0:
            return JsonResponse({'error':'no data'})
        else:
            serializer = DataSerializer(category_data, many=True)
            return JsonResponse(serializer.data,safe=False)

class Search(APIView):
     # find/search based on category
    def post(self,request):
        keywords = json.loads(request.body)
        for key in keywords.keys():
            if key != 'keywords' and key != 'field':
                return JsonResponse({'error':'data format error'})
        # search_pattern = re.compile(f".*{re.escape(keywords['keywords'])}.*", re.IGNORECASE)
        # Perform the search query
        keyword_list=(keywords['keywords'].split(','))
        results=[]
        for keyword in keyword_list:
            results += db.entries.find( { keywords['field']: keyword})
            
        serializer = DataSerializer(results, many=True)
        return JsonResponse(serializer.data,safe=False)
       
# unit tests
# git flow
        