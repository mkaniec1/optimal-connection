from .models import Node, Connection
from geopy import distance

ONE_CHANNEL_PERCENT = 12.5/4800*100  # 12.5 GHz compared to 4.8THz (total capacity)


def find_best(start_node_id: int, end_node_id: int, space: float) -> list[tuple]:
    start_node: Node = Node.objects.get(id=start_node_id)
    end_node: Node = Node.objects.get(id=end_node_id)
    # for heuristic function
    DIST_TO_END = {
        city.id: distance.distance(
            (float(end_node.latitude),
             float(end_node.longitude)),
            (float(city.latitude),
             float(city.longitude))).km
            for city in Node.objects.all()
    }
    LENGTHS = {
        conn.id: distance.distance(
            (float(conn.starting_node.latitude),
             float(conn.starting_node.longitude)),
            (float(conn.ending_node.latitude),
             float(conn.ending_node.longitude))).km
            for conn in Connection.objects.all()
    }
    FINAL_PATHS = [conn.id
                   for conn in Connection.objects.filter(ending_node=end_node)]
    ANTI_PATHS = {
        conn.id: Connection.objects.filter(
            starting_node=conn.ending_node,
            ending_node=conn.starting_node)[0].id
        for conn in Connection.objects.all()
        }
    used_capacity = {
        conn.id: float(conn.provisioned_capacity)
        for conn in Connection.objects.all()
    }
    paths_to_reserve = []
    space_allocation_counter = 0
    while space > 0:
        for conn_id in FINAL_PATHS:
            if used_capacity[conn_id] <= 100 - ONE_CHANNEL_PERCENT:
                break
        else:
            # No possibility of getting to the end node
            return None, space_allocation_counter

        queue = {
            (conn.id,): calculate_q((conn.id,), DIST_TO_END, LENGTHS, used_capacity)
            for conn in Connection.objects.filter(starting_node=start_node)
        }

        while True:
            if not queue:
                return None, space_allocation_counter
            path_to_expand = min(queue, key=queue.get)
            if queue[path_to_expand] == float('inf'):
                return None, space_allocation_counter

            if path_to_expand[-1] in FINAL_PATHS:
                paths_to_reserve.append(path_to_expand)
                space -= 12.5
                space_allocation_counter += 1
                for path in path_to_expand:
                    used_capacity[path] += ONE_CHANNEL_PERCENT
                break

            del queue[path_to_expand]
            new_conns = [conn.id for conn in
                        Connection.objects.filter(
                            starting_node=Connection.objects.get(
                                id=path_to_expand[-1]).ending_node)]
            for new_conn in new_conns:
                if new_conn not in path_to_expand and ANTI_PATHS[new_conn] not in path_to_expand:
                    new_path = (*path_to_expand, new_conn)
                    queue[new_path] = calculate_q(new_path, DIST_TO_END, LENGTHS, used_capacity)
                    if queue[new_path] == float('inf'):
                        del queue[new_path]
    return paths_to_reserve, space_allocation_counter


def calculate_q(conns: tuple[int], dist_to_end, lengths, used):
    used_strength = 5
    value = 0
    conn_ids = list(conns)
    for conn_id in conn_ids:
        if used[conn_id] > 100 - ONE_CHANNEL_PERCENT:
            value = float('inf')
            return value
        value += lengths[conn_id] + used[conn_id] * used_strength
    value += dist_to_end[Connection.objects.get(id=conn_ids[-1]).ending_node.id]
    return value
