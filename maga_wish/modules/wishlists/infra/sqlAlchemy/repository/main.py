from sqlmodel import Session, select
from typing import List, Optional
# from datetime import datetime, timezone

from maga_wish.modules.users.infra.sqlAlchemy.entities.users import User
from maga_wish.modules.wishlists.infra.sqlAlchemy.entities.wishlists import Wishlist
from maga_wish.modules.wishlists.dtos import (
    GetWishlistByUserIdDTO
)

class WishlistRepository:
    # def create(self, *, session: Session, userData: CreateUserDTO) -> User:
    #     user = User.model_validate(
    #         userData, update={"hashed_password": get_password_hash(userData.password)}
    #     )
    #     session.add(user)
    #     session.commit()
    #     session.refresh(user)
    #     return user
    
    def getWishlistByUserId(self, *, session: Session, data: GetWishlistByUserIdDTO) -> Optional[List[Wishlist]]: 
        query = select(Wishlist).where(Wishlist.id == data.id).limit(data.limit).offset(data.limit * (data.page - 1))
        wishlist = session.exec(query).all()

        return wishlist if wishlist else []
    
    # def deleteWishlist(self, *, session: Session, data: DeleteUserDTO) -> bool: 
    #     user = self.getUserById(session=session, userData=GetUserByIdDTO(id=data.id))

    #     user.deleted_at = datetime.now(timezone.utc)

    #     if user:
    #         session.delete(user)
    #         session.commit()
    #         return True
    #     return False