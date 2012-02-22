import abc

class SiftEngine(object):

    __metaclass__ = abc.ABCMeta
    
    def version(self):
        return 0.1

    @abc.abstractmethod
    def is_constructed(self):
        pass
    
        