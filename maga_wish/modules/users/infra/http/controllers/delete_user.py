from typing import Any
from fastapi import APIRouter, Depends, Request, HTTPException
from uuid import UUID

from maga_wish.modules.users.dtos import (
    DeleteUserDTO,
    GetUserByIdDTO
)
from maga_wish.shared.infra.http.utils import (
    CurrentUserDep,
    SessionDep
)
from maga_wish.modules.users.infra.sqlAlchemy.repository.main import UserRepository
from maga_wish.modules.users.services import (
    GetUserByIdService,
    DeleteUserService
)
from maga_wish.shared.infra.http.utils import MessageToReturn


router = APIRouter()

def getUserByIdService(
    userRepository: UserRepository = Depends(UserRepository),
    request: Request = None
) -> GetUserByIdService:
    redis_client = request.app.state.redis
    return GetUserByIdService(userRepository, redis_client)

def deleteUserService(
    userRepository: UserRepository = Depends(UserRepository),
    request: Request = None
) -> DeleteUserService:
    redis_client = request.app.state.redis
    return DeleteUserService(userRepository, redis_client)

@router.delete("/{user_id}", response_model=MessageToReturn)
async def delete_user(
    session: SessionDep,
    _: CurrentUserDep,
    user_id: UUID,
    getUserService: GetUserByIdService = Depends(getUserByIdService),
    deleteUserService: DeleteUserService = Depends(deleteUserService),
) -> Any:
    """
    Delete a user
    """
    data = GetUserByIdDTO(id=user_id)
    user = await getUserService.getUserById(session, data)
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    data = DeleteUserDTO(id=user_id, email=user.email)
    userDeleted = await deleteUserService.deleteUser(session, data)

    if not userDeleted:
        raise HTTPException(
            status_code=500,
            detail="Server Error",
        )
    
    return MessageToReturn(
        success=userDeleted,
        message="User Deleted"
    )