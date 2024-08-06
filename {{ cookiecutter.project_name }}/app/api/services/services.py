from app.config.settings import settings
import logging

class Service:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
