from abc import ABCMeta, abstractmethod


class IParser:
    __metaclass__ = ABCMeta

    @abstractmethod
    def is_review(self):
        pass

    @abstractmethod
    def extract_food_title(self):
        pass

    @abstractmethod
    def extract_price(self):
        pass

    @abstractmethod
    def extract_address(self):
        pass

    @abstractmethod
    def extract_numvote(self):
        pass

    @abstractmethod
    def extract_foodtypes(self):
        pass

    @abstractmethod
    def extract_country(self):
        pass