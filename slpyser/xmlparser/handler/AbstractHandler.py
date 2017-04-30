from abc import abstractmethod
import abc
import sys

if sys.version_info >= (3, 4):
    ABC = abc.ABC
else:
    ABC = abc.ABCMeta('ABC', (), {})

class AbstractHandler(ABC):

    def __init__(self,
                 owner):
        """
        Initson
        :param owner: :class:`~slpyser.xmlparser.SAPLinkContentHandle.SAPLinkContentHandle` object.
        """
        self._owner = owner

    @abstractmethod
    def map_parse(self):
        """
        Should return a Dictionary which maps a tag with three methods to be run at:
        * Start of an element (handles the attributes)
        * Characters of an element (handles all the caracters inside that element which doesn't do part in a nested element)
        * End of an element.

        :rtype: Dictionary
        """
        pass
