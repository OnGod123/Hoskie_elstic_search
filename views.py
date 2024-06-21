# views.py

from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from elasticsearch import Elasticsearch, ElasticsearchException
from elasticsearch_dsl import Search, Q
from .models import UserProfile
import re

@login_required
def search_user_by_query(request):
    if request.method == 'GET':
        query = request.GET.get('query', None)
        if not query or not re.match(r'^[a-zA-Z0-9_@. ]+$', query):
            return HttpResponseBadRequest("Invalid or missing query parameter.")
        
        try:
            client = Elasticsearch()
            s = Search(using=client, index="users").query(
                Q("multi_match", query=query, fields=['username', 'name', 'email'])
            )
            response = s.execute()

            if response.hits.total.value > 0:
                results = []
                for hit in response.hits:
                    try:
                        profile = UserProfile.objects.get(username=hit.username)
                        user_data = {
                            "username": profile.username,
                            "name": profile.name,
                            "email": profile.email,
                            "relationship_status": profile.relationship_status,
                            "sexual_orientation": profile.sexual_orientation,
                            "race": profile.race,
                            "phone_number": profile.phone_number,
                            "social_media_api": profile.social_media_api,
                            "birth_date": profile.birth_date,
                            "profile_video": profile.profile_video.url if profile.profile_video else None,
                            "location": profile.location.name if profile.location else None,
                            "tweet": profile.tweet.url if profile.tweet else None,
                            "video": profile.video.url if profile.video else None,
                            "image": profile.image.url if profile.image else None,
                        }
                        results.append(user_data)
                    except UserProfile.DoesNotExist:
                        continue
                return JsonResponse(results, safe=False)
            else:
                return JsonResponse({"error": "User not found"}, status=404)
        except ElasticsearchException as e:
            return JsonResponse({"error": "Elasticsearch error: " + str(e)}, status=500)
        except Exception as e:
            return JsonResponse({"error": "Server error: " + str(e)}, status=500)

    return HttpResponseBadRequest("Invalid request method.")

