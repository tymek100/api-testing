class _Input:
    def __init__(self, value, absolute=False):
        self.value = value
        self.absolute = absolute

    def __str__(self):
        return self.__class__.__name__.lower()


class Author(_Input):
    pass

class Title(_Input):
    pass

class Lines(_Input):
    pass

class LineCount(_Input):
    pass

class PoemCount(_Input):
    pass

class Random(_Input):
    pass
