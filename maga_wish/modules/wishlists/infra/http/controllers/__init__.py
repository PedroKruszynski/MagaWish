from .get_wishlist_by_user_id import router as get_wishlist_by_user_id
from .add_product_to_wishlist import router as add_product_to_wishlist
from .delete_product_of_wishlist import router as delete_product_of_wishlist

__all__ = [
    "get_wishlist_by_user_id",
    "add_product_to_wishlist",
    "delete_product_of_wishlist"
]
