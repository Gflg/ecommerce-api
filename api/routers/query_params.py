from pydantic import BaseModel, Field
from api.enums import ProductType, SortableProductFields


class QueryParams(BaseModel):
    '''All query parameters used in /api/products GET endpoint.'''
    product_theme: ProductType = Field(
        default=ProductType.DRINK,
        description="Enum for product theme parameters",
    )
    apply_product_theme_filter: bool = False
    product_attribute_to_sort: SortableProductFields = Field(
        default=SortableProductFields.ID,
        description="Enum for sortable product fields parameters",
    )
    apply_product_attribute_sort: bool = False
    descending: bool = False
