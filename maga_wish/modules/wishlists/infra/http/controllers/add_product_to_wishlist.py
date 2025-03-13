from typing import Any
from fastapi import APIRouter, Depends, Request, HTTPException
from uuid import UUID
from typing import List

from maga_wish.modules.wishlists.dtos.wishlist import Wishlist
from maga_wish.modules.users.services import (
    CreateUserService,
    GetUserByIdService
)
from maga_wish.shared.infra.http.utils import SessionDep
from maga_wish.modules.users.infra.sqlAlchemy.repository.main import UserRepository


router = APIRouter()

def addProductToWishlist(
    userRepository: UserRepository = Depends(UserRepository),
    request: Request = None
) -> GetUserByIdService:
    redis_client = request.app.state.redis
    return GetUserByIdService(userRepository, redis_client)

def getUserByIdService(
    userRepository: UserRepository = Depends(UserRepository),
    request: Request = None
) -> GetUserByIdService:
    redis_client = request.app.state.redis
    return GetUserByIdService(userRepository, redis_client)

@router.post("/{user_id}/{product_id}", response_model=List[Wishlist])
async def create_user(
    *,
    session: SessionDep,
    user_id: UUID,
    product_id: UUID,
    addProductToWishlist: CreateUserService = Depends(addProductToWishlist),
    getUserByIdService: GetUserByIdService = Depends(getUserByIdService)
) -> Any:
    """
    Add product to a wishlist
    """
    userExist = await getUserByIdService.getUserById(session, user_id)

    if userExist:
        raise HTTPException(
            status_code=404,
            detail="User not find",
        )

    response = await createUserService.create(session, user)

    return response