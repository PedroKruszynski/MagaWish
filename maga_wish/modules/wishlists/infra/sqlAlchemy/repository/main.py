from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, and_, select

from maga_wish.modules.wishlists.dtos import (
    AddProductToWishlistDTO,
    DeleteProductOfWishlistDTO,
    GetWishlistByUserIdDTO,
    GetWishlistProductByUserIdProductIdDTO,
    RestoreProductOfWishlistDTO,
)
from maga_wish.modules.wishlists.infra.sqlAlchemy.entities.wishlists import Wishlist


class WishlistRepository:
    def create(self, *, session: Session, data: AddProductToWishlistDTO) -> Wishlist:
        try:
            wishlist = Wishlist.model_validate(data)
            session.add(wishlist)
            session.commit()
            session.refresh(wishlist)
            return wishlist
        except IntegrityError:
            session.rollback()
            raise ValueError("This product is already in the wishlist")

    def getWishlistByUserId(
        self, *, session: Session, data: GetWishlistByUserIdDTO
    ) -> list[Wishlist] | None:
        query = (
            select(Wishlist)
            .where(Wishlist.user_id == data.user_id)
            .limit(data.limit)
            .offset(data.limit * (data.page - 1))
        )
        wishlist = session.exec(query).all()

        return wishlist if wishlist else []

    def getWishlistProductByUserIdProductId(
        self, *, session: Session, data: GetWishlistProductByUserIdProductIdDTO
    ) -> Wishlist | None:
        query = select(Wishlist).where(
            and_(
                Wishlist.user_id == data.user_id, Wishlist.product_id == data.product_id
            )
        )
        wishlist = session.exec(query).first()

        return wishlist

    def deleteProductOfWishlist(
        self, *, session: Session, data: DeleteProductOfWishlistDTO
    ) -> bool | None:
        wishlistProduct = self.getWishlistProductByUserIdProductId(
            session=session, data=data
        )

        if not wishlistProduct:
            return None

        if wishlistProduct.deleted_at:
            return False

        if wishlistProduct:
            wishlistProduct.deleted_at = datetime.now(timezone.utc)

            session.commit()
            session.refresh(wishlistProduct)

            return True

        return False

    def restoreProductOfWishlist(
        self, *, session: Session, data: RestoreProductOfWishlistDTO
    ) -> bool | None:
        wishlistProduct = self.getWishlistProductByUserIdProductId(
            session=session, data=data
        )

        if not wishlistProduct:
            return None

        if not wishlistProduct.deleted_at:
            return False

        if wishlistProduct:
            wishlistProduct.deleted_at = None

            session.commit()
            session.refresh(wishlistProduct)

            return True

        return False
