from abc import ABC, abstractmethod
from ..db.db import MongoDatabse


class Resource(ABC):

    def __init__(self):
        self.db = MongoDatabse()