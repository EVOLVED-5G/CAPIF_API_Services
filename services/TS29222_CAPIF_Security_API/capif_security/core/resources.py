from abc import ABC, abstractmethod
from ..db.db import MongoDatabse
from .notification import Notifications

class Resource(ABC):

    def __init__(self):
        self.db = MongoDatabse()
        self.notification = Notifications()