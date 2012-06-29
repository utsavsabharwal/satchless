from ..products.models import OnlineVariantMixin
from satchless.contrib.order.partitioner.simple import SimplePhysicalPartitioner
from satchless.order import Partitioner, Partition
from satchless.order.handler import PartitionerQueue


class OnlinePartitioner(Partitioner):
    shipping = False

    def partition(self, cart, items):
        is_online = lambda x: isinstance(item, OnlineVariantMixin)

        online_items = [item for item in items if is_online(item)]
        other_items = [item for item in items if not is_online(item)]
        return [Partition(online_items, shipping=False)], other_items,


partitioner = PartitionerQueue(OnlinePartitioner,
                               SimplePhysicalPartitioner)
