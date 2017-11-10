

class PropertySignal(object):
    def __init__(self, obj):
        self.__obj = obj
        self.__slots = []

    def __add__(self, slot):
        self.__slots.append(slot)

    def emit(self):
        for slot in self.__slots:
            slot(self.__obj)
