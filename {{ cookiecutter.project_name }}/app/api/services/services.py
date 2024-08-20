from http.client import HTTPException
from app.config.settings import settings
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from .cache_manager import CacheManager
from app.api.schemas.schemas import (
    UserInfo)

class CommonService:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def cached_name(self, prefix: str, identifier: str):
        return f"{prefix}:{identifier}"

    async def generic_user_create(self, crud, data_in, data_name, db: AsyncSession, user: UserInfo):
        self.logger.info(f"Create a new {data_name}")
        self.logger.debug(f"For user {user.uuid} New {data_name} infos {data_in}")

        data_in.user_uuid = user.uuid

        new_data = await crud.create_async(db=db, obj_in=data_in)
        self.logger.info(f"{data_name} created with UUID {new_data.uuid}")
        await CacheManager.store_in_cache(self.cached_name(data_name, new_data.uuid), new_data)
        return new_data

    async def generic_user_get_list(self, crud, data_name, filters, db: AsyncSession, user: UserInfo):
        self.logger.info(f"Get a {data_name} list")
        self.logger.debug(f"For user {user.uuid} {data_name} filter {filters}")

        filters.user_uuid = user.uuid

        datas = await crud.filter_and_paginate_async(db=db, filters=filters.model_dump(exclude_unset=True))
        self.logger.info(f"Fetched {len(datas.items)} {data_name} datas for user {user.uuid}")
        return datas

    async def generic_user_get(self, crud, data_name, uuid: UUID, db: AsyncSession, user: UserInfo):
        self.logger.info(f"Get {data_name} {uuid}")
        self.logger.debug(f"For user {user.uuid}")

        data = await CacheManager.fetch_from_cache(self.cached_name(data_name, uuid))
        if data:
            if data.user is not user.uuid:
                self.logger.debug("error : user not allow to see this story")
                raise HTTPException(status_code=404, detail=f"{data_name} not found")
        else:
            data = await crud.get_async(db=db, id=uuid, user_uuid=user.uuid)
        if not data:
            self.logger.debug("error : data not found")
            raise HTTPException(status_code=404, detail=f"{data_name} not found")
        self.logger.info(f"Fetched {data_name} with UUID {uuid} for user {user.uuid}")
        return data

    async def generic_user_update(self, crud, data_name, uuid: UUID, data_in, db: AsyncSession, user: UserInfo):
        self.logger.info(f"Update {data_name} {uuid}")
        self.logger.debug(f"For user {user.uuid} New {data_name} infos {data_in}")

        data = await crud.get_by_id_and_user_async(db=db, id=uuid, user_uuid=user.uuid)
        if not data:
            self.logger.debug("error : update data not found, verify the data exist")
            raise HTTPException(status_code=404, detail=f"{data_name} not found")
        updated_data = await crud.add_update_async(db=db, db_obj=data, obj_in=data_in)
        await CacheManager.store_in_cache(self.cached_name(data_name, updated_data.uuid), updated_data)
        self.logger.info(f"Updated {data_name} with UUID {uuid} for user {user.uuid}")
        return updated_data

    async def generic_user_delete(self, crud, data_name, uuid: UUID, db: AsyncSession, user: UserInfo):
        self.logger.info(f"Delete {data_name} {uuid}")
        self.logger.debug(f"For user {user.uuid}")

        data = await crud.remove_checking_user_async(db=db, id=uuid, user_uuid=user.uuid)
        if not data:
            self.logger.debug("error : data not found")
            raise HTTPException(status_code=404, detail=f"{data_name} not found")
        await CacheManager.remove_from_cache(self.cached_name(data_name, uuid))
        return True

    async def generic_admin_create(self, crud, data_in, data_name, db: AsyncSession, user: UserInfo):
        self.logger.warn(f"Create a new {data_name}")
        self.logger.debug(f"For admin user {user.uuid} New {data_name} infos {data_in}")

        if not hasattr(data_in, "user_uuid"):
            data_in.user_uuid = user.uuid

        new_data = await crud.create_async(db=db, obj_in=data_in)
        self.logger.info(f"{data_name} created with UUID {new_data.uuid}")
        await CacheManager.store_in_cache(self.cached_name(data_name, new_data.uuid), new_data)
        return new_data

    async def generic_admin_get_list(self, crud, data_name, filters, db: AsyncSession, user: UserInfo):
        self.logger.warn(f"Get a {data_name} list")
        self.logger.debug(f"For admin user {user.uuid} {data_name} filter {filters}")

        datas = await crud.filter_and_paginate_async(db=db, filters=filters.model_dump(exclude_unset=True))
        self.logger.info(f"Fetched {len(datas.items)} {data_name} datas for user {user.uuid}")
        return datas

    async def generic_admin_get(self, crud, data_name, uuid: UUID, db: AsyncSession, user: UserInfo):
        self.logger.warn(f"Get {data_name} {uuid}")
        self.logger.debug(f"For admin user {user.uuid}")

        data = await CacheManager.fetch_from_cache(self.cached_name(data_name, uuid))
        if not data:
            data = await crud.get_async(db=db, id=uuid, user_uuid=user.uuid)
        if not data:
            self.logger.debug("admin error : data not found")
            raise HTTPException(status_code=404, detail=f"{data_name} not found")
        self.logger.info(f"Fetched {data_name} with UUID {uuid} for user {user.uuid}")
        return data

    async def generic_admin_update(self, crud, data_name, uuid: UUID, data_in, db: AsyncSession, user: UserInfo):
        self.logger.warn(f"Update {data_name} {uuid}")
        self.logger.debug(f"For admin user {user.uuid} New {data_name} infos {data_in}")

        data = await crud.get_async(db=db, id=uuid)
        if not data:
            self.logger.debug("admin error : data not found")
            raise HTTPException(status_code=404, detail=f"{data_name} not found")
        updated_data = await crud.add_update_async(db=db, db_obj=data, obj_in=data_in)
        await CacheManager.store_in_cache(self.cached_name(data_name, updated_data.uuid), updated_data)
        self.logger.info(f"Updated {data_name} with UUID {uuid} for user {user.uuid}")
        return updated_data

    async def generic_admin_delete(self, crud, data_name, uuid: UUID, db: AsyncSession, user: UserInfo):
        self.logger.warn(f"Delete {data_name} {uuid}")
        self.logger.debug(f"For admin user {user.uuid}")

        data = await crud.remove_async(db=db, id=uuid)
        if not data:
            self.logger.debug("admin error : data not found")
            raise HTTPException(status_code=404, detail=f"{data_name} not found")
        await CacheManager.remove_from_cache(self.cached_name(data_name, uuid))
        return True


class UserService(CommonService):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)

    def cached_name(self, data: str):
        return f"story {data}"
