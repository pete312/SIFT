import abc
import siftproperty

class SiftEngine(object):

    __metaclass__ = abc.ABCMeta
    
    def version(self):
        return siftproperty.version()

    @abc.abstractmethod
    def is_constructed(self):
        pass
    
        