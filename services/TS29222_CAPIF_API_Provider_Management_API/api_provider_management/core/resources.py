from abc import ABC, abstractmethod
from ..db.db import MongoDatabse
from .publisher import Publisher

class Resource(ABC):

    def __init__(self):
        self.db = MongoDatabse()
        self.publish_ops = Publisher()