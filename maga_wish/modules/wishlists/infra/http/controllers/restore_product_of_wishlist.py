from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from maga_wish.modules.wishlists.dtos import RestoreProductOfWishlistDTO
from maga_wish.modules.wishlists.infra.sqlAlchemy.repository.main import (
    WishlistRepository,
)
from maga_wish.modules.wishlists.services import RestoreProductOfWishlistService
from maga_wish.shared.infra.http.utils import MessageToReturn, SessionDep

router = APIRouter()


def restoreProductOfWishlistService(
    wishlistRepository: WishlistRepository = Depends(WishlistRepository),
) -> RestoreProductOfWishlistService:
    return RestoreProductOfWishlistService(wishlistRepository)


@router.put("/{user_id}/{product_id}", response_model=MessageToReturn)
async def restore_product_of_wishlist(
    *,
    session: SessionDep,
    user_id: UUID,
    product_id: UUID,
    restoreProductOfWishlistService: RestoreProductOfWishlistService = Depends(
        restoreProductOfWishlistService
    ),
) -> Any:
    """
    Restore a product of a wishlist
    """
    data = RestoreProductOfWishlistDTO(user_id=user_id, product_id=product_id)
    productRestored = await restoreProductOfWishlistService.restoreProduct(
        session, data
    )

    if not productRestored:
        raise HTTPException(
            status_code=404,
            detail="Product not exist in the wishlist",
        )

    return MessageToReturn(
        success=productRestored, message="Product restored from the wishlist"
    )
