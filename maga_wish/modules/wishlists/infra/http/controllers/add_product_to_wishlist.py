from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request

from maga_wish.modules.products.dtos import GetProductByIdDTO
from maga_wish.modules.products.services import GetProductByIdService
from maga_wish.modules.users.dtos import GetUserByIdDTO
from maga_wish.modules.users.infra.sqlAlchemy.repository.main import UserRepository
from maga_wish.modules.users.services import GetUserByIdService
from maga_wish.modules.wishlists.dtos import (
    AddProductToWishlistDTO,
    GetWishlistByUserIdDTO,
)
from maga_wish.modules.wishlists.dtos.wishlist import Wishlist
from maga_wish.modules.wishlists.infra.sqlAlchemy.repository.main import (
    WishlistRepository,
)
from maga_wish.modules.wishlists.services import (
    AddProductToWishlistService,
    GetWishlistByUserIdService,
)
from maga_wish.shared.infra.http.utils import SessionDep

router = APIRouter()


def addProductToWishlistService(
    wishlistRepository: WishlistRepository = Depends(WishlistRepository),
) -> AddProductToWishlistService:
    return AddProductToWishlistService(wishlistRepository)


def getWishlistByUserIdService(
    wishlistRepository: WishlistRepository = Depends(WishlistRepository),
) -> GetWishlistByUserIdService:
    return GetWishlistByUserIdService(wishlistRepository)


def getUserByIdService(
    userRepository: UserRepository = Depends(UserRepository), request: Request = None
) -> GetUserByIdService:
    redis_client = request.app.state.redis
    return GetUserByIdService(userRepository, redis_client)


def getProductByIdService() -> GetProductByIdService:
    return GetProductByIdService()


@router.post("/{user_id}/{product_id}", response_model=list[Wishlist])
async def add_product_to_wishlist(
    *,
    session: SessionDep,
    user_id: UUID,
    product_id: UUID,
    addProductToWishlistService: AddProductToWishlistService = Depends(
        addProductToWishlistService
    ),
    getUserByIdService: GetUserByIdService = Depends(getUserByIdService),
    getProductByIdService: GetProductByIdService = Depends(getProductByIdService),
    getWishlistByUserIdService: GetWishlistByUserIdService = Depends(
        getWishlistByUserIdService
    ),
) -> Any:
    """
    Add product to a wishlist
    """
    dataFindUser = GetUserByIdDTO(id=user_id)
    userExist = await getUserByIdService.getUserById(session, dataFindUser)

    if not userExist:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    dataFindProduct = GetProductByIdDTO(id=product_id)
    productExist = await getProductByIdService.getProductById(dataFindProduct)

    if "error" in productExist and productExist["error"]:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    dataToCreate = AddProductToWishlistDTO(user_id=user_id, product_id=product_id)

    try:
        await addProductToWishlistService.create(session, dataToCreate)

        dataToFindWhislist = GetWishlistByUserIdDTO()
        dataToFindWhislist.user_id = user_id
        wishlistOfUser = await getWishlistByUserIdService.getWishlistByUserId(
            session=session, data=dataToFindWhislist
        )

        return wishlistOfUser
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )
