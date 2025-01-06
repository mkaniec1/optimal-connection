from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from . import models, a_star
import json

@ensure_csrf_cookie
def api_connections(request):
    cities = models.Node.objects.all()
    context_cities = [
        (city.id, city.latitude, city.longitude) for city in cities
    ]
    connections = models.Connection.objects.all()
    context_connections = [
        (conn.id,
         conn.starting_node.id,
         conn.ending_node.id,
         conn.total_capacity,
         conn.provisioned_capacity)
        for conn in connections
    ]
    context = {
        "cities": context_cities,
        "connections": context_connections,
    }

    return JsonResponse(
        context
    )


def api_reserve(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        start_node = data.get('startNode')
        end_node = data.get('endNode')
        best_route = a_star.find_best(start_node, end_node)
        return JsonResponse(
            {'bestRoute': best_route},
        )