from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from . import models, a_star, tools
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
        speed = int(data.get('speed'))
        solver = a_star.AStarOptimalPathSolver()
        best_route = solver.solve(start_node, end_node, speed)
        if not best_route:
            return JsonResponse(
                {'error': "Choose desired speed!"},
                status=400
            )
        channel_size = solver.translate_to_channel(speed)
        tools.add_channel_to_db(best_route, channel_size)
        best_route = [str(conn) for conn in best_route]
        return JsonResponse(
            {'bestRoute': best_route,
             'channelSize': channel_size},
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
        "25.0": 0,
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
