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
        space = float(data.get('space'))
        best_routes, times_allocated = a_star.find_best(start_node, end_node, space)
        if not best_routes:
            return JsonResponse(
                {'error': f"Maximum number of allocations is {times_allocated}, which is {times_allocated*12.5} GHz."},
                status=400
            )
        unique_best_routes = set(best_routes)
        message = []
        for route in unique_best_routes:
            message.append({
                'route': route,
                'count': best_routes.count(route)
            })
        return JsonResponse(
            {'bestRoutes': message},
        )
