
import asyncio


class PropertySignal(object):
    def __init__(self, obj):

        self.__obj = obj
        self.__slots = []

    def __add__(self, slot):
        self.__slots.append(slot)
        return self

    def emit(self):
        for slot in self.__slots:
            asyncio.ensure_future(slot(self.__obj))
