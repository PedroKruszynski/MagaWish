from typing import Any, List
from fastapi import APIRouter, Depends, Query

from maga_wish.modules.wishlists.dtos.wishlist import Wishlist
from maga_wish.modules.users.infra.sqlAlchemy.repository.main import UserRepository
from maga_wish.modules.users.services import GetUsersService
from maga_wish.modules.wishlists.dtos import GetWishlistByUserIdDTO
from maga_wish.shared.infra.http.utils import (
    CurrentUserDep,
    SessionDep
)

router = APIRouter()

def getUsersService(
    userRepository: UserRepository = Depends(UserRepository),
) -> GetUsersService:
    return GetUsersService(userRepository)

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
    data: GetWishlistByUserIdDTO = Depends(getWishlistDto),
    getUsersService: GetUsersService = Depends(getUsersService),
) -> Any:
    """
    Get a wishlist
    """
    users = await getUsersService.getUsers(session, data)
    return users