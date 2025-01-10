from time import sleep
from .models import Node, Connection
from geopy import distance


class AStarOptimalPathSolver():
    def __init__(self):
        self.ONE_CHANNEL_PERCENT = 12.5/4800*100  # 12.5 GHz compared to 4.8THz (total capacity)

    def end_blocked(self):
        for conn_id in self.FINAL_PATHS:
            if self.used_capacity[conn_id] <= 100 - self.ONE_CHANNEL_PERCENT:
                return False
        return True

    def calculate_q(self, path: tuple[int]):
        value = 0
        conn_ids = list(path)
        for conn_id in conn_ids:
            if self.used_capacity[conn_id] > 100 - self.ONE_CHANNEL_PERCENT:
                value = float('inf')
                return value
            value += self.LENGTHS[conn_id] + self.calculate_penalty(conn_id)
        value += self.DIST_TO_END[path[-1]]
        return value

    def calculate_penalty(self, conn_id):
        usage = self.used_capacity[conn_id]
        if usage < 50:
            return 0
        if usage < 90:
            return (usage-50)*3
        return self.LENGTHS_SUM

    def add_path_to_reserve(self, path: tuple, reserved_paths: list[tuple]):
        reserved_paths.append(path)
        for conn_id in path:
            self.used_capacity[conn_id] += self.ONE_CHANNEL_PERCENT

    def solve(self, start_node_id: int, end_node_id: int, space: float):
        self.load_data(start_node_id, end_node_id)
        paths_to_reserve: list[tuple] = []
        space_allocation_counter: int = 0

        while space > 0:
            if self.end_blocked():
                return None, space_allocation_counter

            queue = {
                (conn.id,): self.calculate_q((conn.id,))
                for conn in self.starting_conns
            }

            while True:
                if not queue:
                    return None, space_allocation_counter
                path_to_expand = min(queue, key=queue.get)

                if queue[path_to_expand] == float('inf'):
                    return None, space_allocation_counter

                if path_to_expand[-1] in self.FINAL_PATHS:
                    self.add_path_to_reserve(path_to_expand, paths_to_reserve)
                    space -= 12.5
                    space_allocation_counter += 1
                    break

                del queue[path_to_expand]

                new_conns = self.continuations[path_to_expand[-1]]
                for new_conn in new_conns:
                    if self.not_repeated(new_conn, path_to_expand):
                        new_path = (*path_to_expand, new_conn)
                        new_path_value = self.calculate_q(new_path)
                        if new_path_value != float('inf'):
                            queue[new_path] = new_path_value

        return paths_to_reserve, space_allocation_counter

    def not_repeated(self, conn, path):
        return conn not in path and self.ANTI_PATHS[conn] not in path

    def load_data(self, start_node_id, end_node_id):
        self.start_node: Node = Node.objects.get(id=start_node_id)
        self.end_node: Node = Node.objects.get(id=end_node_id)
        self.DIST_TO_END = {
            conn.id: distance.distance(
                (float(self.end_node.latitude),
                 float(self.end_node.longitude)),
                (float(conn.ending_node.latitude),
                 float(conn.ending_node.longitude))).km
            for conn in Connection.objects.all()
        }
        self.LENGTHS = {
            conn.id: distance.distance(
                (float(conn.starting_node.latitude),
                 float(conn.starting_node.longitude)),
                (float(conn.ending_node.latitude),
                 float(conn.ending_node.longitude))).km
            for conn in Connection.objects.all()
        }
        self.LENGTHS_SUM = sum(self.LENGTHS.values())
        self.FINAL_PATHS = [conn.id for conn in
                            Connection.objects.filter(
                                ending_node=self.end_node
                            )]
        self.ANTI_PATHS = {
            conn.id: Connection.objects.filter(
                starting_node=conn.ending_node,
                ending_node=conn.starting_node)[0].id
            for conn in Connection.objects.all()
        }
        self.used_capacity = {
            conn.id: float(conn.provisioned_capacity)
            for conn in Connection.objects.all()
        }
        self.starting_conns = Connection.objects.filter(starting_node=self.start_node)
        self.continuations = {
            conn.id: [
                later_conn.id for later_conn in Connection.objects.filter(
                    starting_node=conn.ending_node
                )
            ]
            for conn in Connection.objects.all()
        }
