from optimal_path.models import Node, Connection, Channel
from django.db.models import Q
import csv


def load_nodes():
    with open("optimal_path/initial_data/wezly.csv", "r") as file:
        reader = csv.reader(file, delimiter=";")
        headers = next(reader)
        for row in reader:
            node_id, latitude, longitude = row
            Node.objects.create(
                id=int(node_id),
                latitude=float(latitude.replace(",", ".")),
                longitude=float(longitude.replace(",", "."))
            )


def load_connections():
    with open("optimal_path/initial_data/zajetosc.csv", "r") as file:
        reader = csv.reader(file, delimiter=";")
        headers = next(reader)
        for row in reader:
            connection_id = row[0]
            starting_node = Node.objects.get(id=row[1])
            ending_node = Node.objects.get(id=row[2])
            total_capacity = row[3][:-4]  # to remove " THz"
            provisioned_capacity = row[4]

            Connection.objects.create(
                id=connection_id,
                starting_node=starting_node,
                ending_node=ending_node,
                total_capacity=total_capacity,
                provisioned_capacity=provisioned_capacity,
            )


def load_channels():
    with open("optimal_path/initial_data/spectrum_kanaly.csv", "r") as file:
        reader = csv.reader(file, delimiter=";")
        headers = next(reader)
        for row in reader:
            connection_id = row[0]
            if not row[1] or not row[2] or not row[3]:
                continue
            request_free_id = row[1]
            frequency = row[2]
            width = float(row[3])
            if width == 37.5:
                width = 50.0
            elif width == 59.0:
                width = 75.0
            elif width == 101.8:
                width = 112.5
            else:
                raise ValueError(f"unexpected value: {width}")
            # row[4] skipped
            channel = row[5]
            Channel.objects.create(
                connection=Connection.objects.filter(id=connection_id)[0],
                request_free_id=request_free_id,
                frequency=frequency,
                width=width,
                channel=channel,
            )


def load_all():
    load_nodes()
    load_connections()
    load_channels()
    delete_orphan_nodes()


def delete_orphan_nodes():
    orphan_nodes = Node.objects.filter(
        ~Q(id__in=Connection.objects.values_list('starting_node', flat=True)) &
        ~Q(id__in=Connection.objects.values_list('ending_node', flat=True))
    )
    orphan_nodes.delete()
