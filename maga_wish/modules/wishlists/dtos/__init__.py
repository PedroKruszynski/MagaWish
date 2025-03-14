from .add_product_to_wishlist_dto import AddProductToWishlistDTO
from .delete_product_of_wishlist_dto import DeleteProductOfWishlistDTO
from .get_wishlist_by_user_id_dto import GetWishlistByUserIdDTO
from .get_wishlist_product_by_user_id_product_id_dto import (
    GetWishlistProductByUserIdProductIdDTO,
)
from .restore_product_of_wishlist_dto import RestoreProductOfWishlistDTO

__all__ = [
    "GetWishlistByUserIdDTO",
    "AddProductToWishlistDTO",
    "DeleteProductOfWishlistDTO",
    "GetWishlistProductByUserIdProductIdDTO",
    "RestoreProductOfWishlistDTO",
]
