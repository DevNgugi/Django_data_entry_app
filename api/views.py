
import json
import re
from rest_framework import status
from django.http import JsonResponse,HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from pymongo import MongoClient
from api.serializers import DataSerializer
from .encoder import JsonEncoder
# connection string
connection_string='mongodb://localhost:27017'
client=MongoClient(connection_string)

# get database
db=client.get_database('demo_database')
   
class Entries(APIView):
    def get(self,request):
        all_entries= list(db.entries.find())
        if (len(all_entries)) == 0:
            return Response(data={'error':'no data'}, status=status.HTTP_204_NO_CONTENT)
        
        else:
            # serializer = DataSerializer(all_entries, many=True)
            # return HttpResponse(all_entries)
            return Response(json.loads(json.dumps(all_entries, cls=JsonEncoder)), status=status.HTTP_200_OK)
 
    def post(self,request):
        # return Response(data={'message':'message'}, status=status.HTTP_403_FORBIDDEN)
        
        entry = json.loads(request.body)
        # check whether the passed json has only category and data as the top level keys*
        for key in entry.keys():
            if key == 'category':
                db.entries.insert_one(entry)
                return Response(data={'success':'data saved'}, status=status.HTTP_201_CREATED)
                
                # return JsonResponse({'success':'data saved','status':status.HTTP_201_CREATED})                
            else:
                return Response(data={'error':'missing category key'}, status=status.HTTP_403_FORBIDDEN)
                
                # return JsonResponse({'error':'missing category key','status':status.HTTP_403_FORBIDDEN})
        
class Category(APIView):
     # find/search based on category
    def post(self,request, ):
       
        category = json.loads(request.body)
        # only category field should be passed
        for key in category.keys():
            if key != 'category':
                return Response(data={'error':'data format error'}, status=status.HTTP_403_FORBIDDEN)

        category_data= list(db.entries.find( { "category": category['category']}))
        if (len(category_data)) == 0:
            return Response(data={'error':'no data'}, status=status.HTTP_204_NO_CONTENT)
        
        else:
            return Response(json.loads(json.dumps(category_data, cls=JsonEncoder)), status=status.HTTP_200_OK)

class Search(APIView):
     # find/search based on keywords passed on as a comma separated string
    def post(self,request):
        keywords = json.loads(request.body)
        for key in keywords.keys():
            if key != 'keywords' and key != 'field':
                # return JsonResponse({'error':'data format error'})
                return Response(data={'error':'data format error'}, status=status.HTTP_403_FORBIDDEN)

        keyword_list=(keywords['keywords'].split(','))
        results=[]
        for keyword in keyword_list:
            search_pattern = re.compile(f".*{re.escape(keyword.strip())}.*", re.IGNORECASE)

            results += db.entries.find( { keywords['field']: {"$regex": search_pattern}})
            
        return Response(json.loads(json.dumps(results, cls=JsonEncoder)), status=status.HTTP_200_OK)
       
        