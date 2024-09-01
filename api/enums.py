from enum import Enum


class ProductType(str, Enum):
    '''Used to enumerate all possible product themes in database.'''
    DRINK = 'drink'
    FOOD = 'food'
    PERSONAL_CARE = 'personal_care'
    HEALTH_CARE = 'health_care'
    CLEANING = 'cleaning'


class SortableProductFields(str, Enum):
    '''
    Used to enumerate all possible product attributes
    which can be used on sorting.
    '''
    ID = 'id'
    NAME = 'name'
    THEME = 'theme'
    PRICE = 'price'
    QUANTITY = 'quantity'
