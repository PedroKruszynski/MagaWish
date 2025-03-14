from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from maga_wish.modules.wishlists.dtos import DeleteProductOfWishlistDTO
from maga_wish.modules.wishlists.infra.sqlAlchemy.repository.main import (
    WishlistRepository,
)
from maga_wish.modules.wishlists.services import DeleteProductOfWishlistService
from maga_wish.shared.infra.http.utils import MessageToReturn, SessionDep

router = APIRouter()


def deleteProductOfWishlistService(
    wishlistRepository: WishlistRepository = Depends(WishlistRepository),
) -> DeleteProductOfWishlistService:
    return DeleteProductOfWishlistService(wishlistRepository)


@router.delete("/{user_id}/{product_id}", response_model=MessageToReturn)
async def delete_product_of_wishlist(
    *,
    session: SessionDep,
    user_id: UUID,
    product_id: UUID,
    deleteProductOfWishlistService: DeleteProductOfWishlistService = Depends(
        deleteProductOfWishlistService
    ),
) -> Any:
    """
    Delete product of a wishlist
    """
    data = DeleteProductOfWishlistDTO(user_id=user_id, product_id=product_id)
    productDeleted = await deleteProductOfWishlistService.deleteProduct(session, data)

    if not productDeleted:
        raise HTTPException(
            status_code=404,
            detail="Product not exist in the wishlist",
        )

    return MessageToReturn(
        success=productDeleted, message="Product deleted from the wishlist"
    )
