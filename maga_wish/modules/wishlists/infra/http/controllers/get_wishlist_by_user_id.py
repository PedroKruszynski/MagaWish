from typing import Any, List
from fastapi import APIRouter, Depends, Query
from uuid import UUID

from maga_wish.modules.wishlists.dtos.wishlist import Wishlist
from maga_wish.modules.wishlists.dtos import GetWishlistByUserIdDTO
from maga_wish.modules.wishlists.services import GetWishlistByUserIdService
from maga_wish.modules.wishlists.infra.sqlAlchemy.repository.main import WishlistRepository 
from maga_wish.shared.infra.http.utils import (
    CurrentUserDep,
    SessionDep
)

router = APIRouter()

def getWishlistByUserIdService(
    userRepository: WishlistRepository = Depends(WishlistRepository),
) -> GetWishlistByUserIdService:
    return GetWishlistByUserIdService(userRepository)

def getWishlistDto(
    limit: int = Query(10, gt=0), 
    page: int = Query(1, gt=0)
) -> GetWishlistByUserIdDTO:
    return GetWishlistByUserIdDTO(limit=limit, page=page)

@router.get("/{user_id}", response_model=List[Wishlist])
async def get_wishlist_by_user_id(
    *,
    session: SessionDep,
    _: CurrentUserDep,
    user_id: UUID,
    data: GetWishlistByUserIdDTO = Depends(getWishlistDto),
    getWishlistByUserIdService: GetWishlistByUserIdService = Depends(getWishlistByUserIdService),
) -> Any:
    """
    Get a wishlist
    """

    data.id = user_id
    wishlist = await getWishlistByUserIdService.getWishlistByUserId(session, data)
    return wishlist