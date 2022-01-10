from abc import abstractmethod


class AbstractAchivement():
    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def achive(self):
        pass