from math import ceil


class Pagination:
    def __init__(self, quantity, page, elements_on_page):
        self.__quantity = quantity
        self.__elements_on_page = elements_on_page
        self.__quantity_page = ceil(self.__quantity / self.__elements_on_page)
        self.page = page % self.__quantity_page

    @property
    def range_elements(self):
        first_element = self.page * self.__elements_on_page
        last_element = min(first_element + self.__elements_on_page, self.__quantity)
        return range(first_element, last_element)
