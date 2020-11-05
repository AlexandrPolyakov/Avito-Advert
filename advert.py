# -*- coding: utf-8 -*-
import json
from typing import Dict, Union


class JSONConverter:
    """Класс, экземпляры которого позволяют обращаться к полям через точку
    :param mapping: Словарь, полученный из JSON
    :type mapping: Dict[str, Union[int, str]]
    """

    def __init__(self, mapping: Dict[str, Union[int, str]]):
        for key, value in mapping.items():
            if isinstance(value, dict):
                setattr(self, key, JSONConverter(value))
            else:
                setattr(self, key, value)


class ColorizeMixin:
    """Mixin для изменения цвета вывода"""

    def __repr__(self):
        return f"\033[1;{self.repr_color_code};20m" \
               f" {self.title} | {self.price} ₽"


class Advert(ColorizeMixin, JSONConverter):
    """Класс, готовящий объекты в финальном виде
    :param repr_color_code: Цвет текста
    :type mapping: int
    """
    repr_color_code: int = 33

    @property
    def price(self) -> int:
        """Свойство цена

        :rtype: int
        :return: Цена или ноль при отстутствии
        """
        try:
            return self._price
        except AttributeError:
            return 0

    @price.setter
    def price(self, value: int):
        """Присвоение цене, проверка на положительность
        :param value: Присваемое значение
        :type value: int
        """
        if value < 0:
            raise ValueError('price must be >= 0')
        else:
            self._price = value


if __name__ == "__main__":
    # Пример из задания
    lesson_str = """{
        "title": "python",
        "price": 1,
        "location": {
            "address": "город Москва, Лесная, 7",
            "metro_stations": ["Белорусская"]
        }
    }"""
    # Пример с отсутствующей ценой
    lesson_empty_price_str = """{
        "title": "python",
        "location": {
            "address": "город Москва, Лесная, 7",
            "metro_stations": ["Белорусская"]
        }
    }"""
    # Пример с отрицательной ценой
    lesson_negative_price_str = """{
        "title": "python",
        "price": 1,
        "location": {
            "address": "город Москва, Лесная, 7",
            "metro_stations": ["Белорусская"]
        }
    }"""
    # Пример с более глубокой иерархией
    deep_lesson_str = """{
        "title": "python",
        "price": 1,
        "location": {
            "Country": {
                "City": "Moscow"
            }
        }
    }"""
    # Пример из задания
    phone_str = """{
        "title": "IPhone X",
        "price": 100
    }"""
    # Пример из задания
    metro_stations_str = """{
        "title": "iPhone X",
        "price": 100,
        "location": {
            "address": "город Самара, улица Мориса Тореза, 50",
            "metro_stations": ["Спортивная", "Гагаринская"]
        }
    }"""
    # Пример из задания
    class_str = """{
        "title": "Вельш-корги",
        "price": 1000,
        "class_": "dogs",
        "location": {
            "address": "сельское поселение Ельдигинское, \
                поселок санатория Тишково, 25"
        }
    }"""
    # Преобразования из JSON в словари
    lesson = json.loads(lesson_str)
    lesson2 = json.loads(lesson_empty_price_str)
    lesson3 = json.loads(lesson_negative_price_str)
    lesson4 = json.loads(deep_lesson_str)
    phone = json.loads(phone_str)
    metro_stations = json.loads(metro_stations_str)
    category = json.loads(class_str)
    # Получение объектов класса Advert
    lesson_ad = Advert(lesson)
    lesson2_ad = Advert(lesson2)
    lesson4_ad = Advert(lesson4)
    phone_ad = Advert(phone)
    metro_stations_ad = Advert(metro_stations)
    category_ad = Advert(category)

    print('phone_ad: ', phone_ad)  # Проверка __repr__
    print('lesson_ad.price: ', lesson_ad.price)  # Проверка вывода цены
    print(
        'lesson2_ad.price: ',
        lesson2_ad.price
    )  # Проверка вывода нулевой цены

    print(
        'lesson_ad.location.address: ',
        lesson_ad.location.address
    )  # Проверка более глубокой иерархии

    print(
        'category_ad.class_: ',
        category_ad.class_
    )  # Проверка вывода атрибута

    print('category_ad: ', category_ad)  # Проверка __repr__

    print(
        'lesson4_ad.location.Country.City: ',
        lesson4_ad.location.Country.City
    )  # Проверка более глубокой иерархии
