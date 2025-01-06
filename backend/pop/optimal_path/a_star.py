from .models import Node, Connection
from geopy import distance


def find_best(start_node_id: int, end_node_id: int):
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
    USED_CAPACITY = {
        conn.id: float(conn.provisioned_capacity)
        for conn in Connection.objects.all()
    }

    queue = {
        (conn.id,): calculate_q((conn.id,), DIST_TO_END, LENGTHS, USED_CAPACITY)
        for conn in Connection.objects.filter(starting_node=start_node)
    }
    i = 0
    while True:
        path_to_expand = min(queue, key=queue.get)
        print(i, ": ", end="\n")
        for path, length in queue.items():
            print(path)
            print(length)
        print("============")
        i += 1
        if path_to_expand[-1] in FINAL_PATHS:
            return path_to_expand
        del queue[path_to_expand]
        new_conns = [conn.id for conn in
                     Connection.objects.filter(
                         starting_node=Connection.objects.get(
                             id=path_to_expand[-1]).ending_node)]
        for new_conn in new_conns:
            if new_conn not in path_to_expand and new_conn != ANTI_PATHS[path_to_expand[-1]]:
                new_path = (*path_to_expand, new_conn)
                queue[new_path] = calculate_q(new_path, DIST_TO_END, LENGTHS, USED_CAPACITY)


def calculate_q(conns: tuple[int], dist_to_end, lengths, used):
    used_strength = 3
    value = 0
    conn_ids = list(conns)
    for conn_id in conn_ids:
        value += lengths[conn_id] + used[conn_id] * used_strength
    value += dist_to_end[Connection.objects.get(id=conn_ids[-1]).ending_node.id]
    return value
