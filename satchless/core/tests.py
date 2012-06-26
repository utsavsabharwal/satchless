from django.test import TestCase
from ..core.handler import QueueHandler
from ..pricing.handler import PricingHandler

class QueueHandlerTestCase(TestCase):
    def setUp(self):
        self.queue_handler = QueueHandler(PricingHandler(), PricingHandler(),
                                                            PricingHandler())
        
    def test_queue_len(self):
        queue_len = len(self.queue_handler.queue)
        
        self.assertEquals(queue_len, 3)