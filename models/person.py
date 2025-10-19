from abc import ABC, abstractmethod

class Person(ABC):
    """
    Abstract class representing a general person in the system.
    """

    def __init__(self, name: str, email: str):
        self._name = name
        self._email = email

    # ---------- Encapsulation ----------
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value

    @property
    def email(self) -> str:
        return self._email

    @abstractmethod
    def display_info(self):
        """Abstract method that must be implemented by subclasses"""
        pass
