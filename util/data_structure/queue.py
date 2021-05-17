from models.token import Token


class Queue:
    def __init__(self, elements: list):
        self.__elements: list[Token] = elements
        self.__first_index = 0

    def is_not_empty(self) -> bool:
        return len(self.__elements) > self.__first_index

    def add(self, value) -> None:
        self.__elements.append(value)

    def remove(self) -> Token:
        if self.is_not_empty():
            self.__first_index += 1
            return self.__elements[self.__first_index - 1]

    def peek(self) -> Token:
        if self.is_not_empty():
            return self.__elements[self.__first_index]
