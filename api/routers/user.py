from fastapi import APIRouter, status, Depends

from api.request import CreateUserRequestSchema, UpdateUserRequestSchema
from api.response import (
    GetUserResponseSchema,
    GetUsersResponseSchema,
    CreateUserResponseSchema,
    UpdateUserResponseSchema
)
from app.services import UserService
from core.db.models import UserModel
from core.fastapi.dependencies import check_permission

router = APIRouter(
    prefix="/api/users",
    tags=["Users"],
)

@router.get(
    path="/{user_id}",
    response_model=GetUserResponseSchema,
    status_code=status.HTTP_200_OK
)
async def get_user(user_id: int):
    return await UserService.get_user_by_id(user_id)


@router.get(
    path="",
    response_model=list[GetUsersResponseSchema],
    openapi_extra={"permissions": UserModel.ADMIN},
    status_code=status.HTTP_200_OK
)
async def get_users(
        limit: int | None = 10,
        offset: int | None = 0,
        permissions = Depends(check_permission)
):
    return await UserService.get_all_users(limit=limit, offset=offset)


@router.post(
    path="/create",
    openapi_extra={"permissions": UserModel.ADMIN},
    response_model=CreateUserResponseSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_user(
        body: CreateUserRequestSchema,
        permissions = Depends(check_permission)
):
    return await UserService.create_user(body=body)


@router.patch(
    path="/update/{user_id}",
    openapi_extra={"permissions": UserModel.ADMIN},
    status_code=status.HTTP_201_CREATED,
    response_model=UpdateUserResponseSchema
)
async def update_user(
        user_id: int,
        body: UpdateUserRequestSchema,
        permissions = Depends(check_permission)
):
    return await UserService.update_user(user_id=user_id, body=body)


@router.delete(
    path="/delete/{user_id}",
    openapi_extra={"permissions": UserModel.ADMIN},
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user(
        user_id: int,
        permissions = Depends(check_permission)
):
    await UserService.delete_user(user_id)
