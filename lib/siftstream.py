import abc

class SiftStream(object):

    __metaclass__ = abc.ABCMeta
    
    def version(self):
        return 0.1

    @abc.abstractmethod
    def write(self):
        pass
    
    @abc.abstractmethod
    def read(self):
        pass
    