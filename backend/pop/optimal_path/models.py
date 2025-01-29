from django.db import models


class Node(models.Model):
    latitude = models.DecimalField("Latitude", max_digits=16, decimal_places=14)
    longitude = models.DecimalField("Longitude", max_digits=16, decimal_places=14)


class Connection(models.Model):
    starting_node = models.ForeignKey(Node, on_delete=models.DO_NOTHING, related_name="start_connections")
    ending_node = models.ForeignKey(Node, on_delete=models.DO_NOTHING, related_name="end_connections")
    total_capacity = models.DecimalField("Total capacity", max_digits=4, decimal_places=1)
    provisioned_capacity = models.DecimalField("Provisioned capacity", max_digits=5, decimal_places=2)


class Channel(models.Model):
    connection = models.ForeignKey(Connection, on_delete=models.DO_NOTHING)
    request_free_id = models.CharField("Request Free Id", max_length=64, null=True)
    frequency = models.DecimalField("Frequency", max_digits=9, decimal_places=6, null=True)
    width = models.DecimalField("Width", max_digits=4, decimal_places=1)
    channel = models.CharField("Channel name", max_length=5, null=True)
