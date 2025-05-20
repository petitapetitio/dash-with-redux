import abc

from city import City


class Client(abc.ABC):

    @abc.abstractmethod
    def get_cities(self) -> list[City]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_city(self, city: City):
        raise NotImplementedError


class InMemoryClient(Client):
    def __init__(self):
        self._cities: list[City] = []

    def get_cities(self) -> list[City]:
        return self._cities

    def add_city(self, city: City):
        self._cities.append(city)
