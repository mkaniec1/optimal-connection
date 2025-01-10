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
        (str(conn.id),
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
        solver = a_star.AStarOptimalPathSolver()
        best_routes, times_allocated = solver.solve(start_node, end_node, space)
        if not best_routes:
            return JsonResponse(
                {'error': f"Maximum number of allocations is {times_allocated}, which is {times_allocated*12.5} GHz."},
                status=400
            )
        unique_best_routes = set(best_routes)
        message = []
        for route in unique_best_routes:
            str_route = ()
            for conn in route:
                str_route = (*str_route, str(conn))
            message.append({
                'route': str_route,
                'count': best_routes.count(route)
            })
        return JsonResponse(
            {'bestRoutes': message},
        )


def api_get_channels(request, conn_id):
    conn = models.Connection.objects.get(id=conn_id)
    orange = conn.starting_node.id
    purple = conn.ending_node.id
    capacity = conn.provisioned_capacity
    secondConn = models.Connection.objects.filter(
        starting_node=conn.ending_node,
        ending_node=conn.starting_node)[0].id
    channels = {
        "12.5": 0,
        "50.0": 0,
        "75.0": 0,
        "112.5": 0
    }
    for channel in models.Channel.objects.filter(connection=conn):
        width = str(channel.width)
        channels[width] += 1

    return JsonResponse({
        "orange": orange,
        "purple": purple,
        "capacity": str(float(capacity)),
        "firstConn": conn_id,
        "secondConn": secondConn,
        "channels": channels,
    })
