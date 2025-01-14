# IUserRepository를 인터페이스 삼아서 실제 로직 구현
# 내부 시스템이 사용하고자 하는 외부 시스템을 다룸
# ex) 데이터베이스에 저장된 데이토를 조회하는 SQL이 인프라 계층에 있어야 함

from user.domain.repository.user_repo import IUserRepository
from user.domain.user import User
from user.infra.db_models.users import Users
from sqlalchemy.exc import SQLAlchemyError
from fastapi.exceptions import HTTPException
from fastapi import status
from database import SessionLocal
from user.domain.user import User as UserVO
from utils.db_utils import row_to_dict
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(IUserRepository):
    async def find_by_id(self, id: str):
        async with SessionLocal() as db:
            result = await db.execute(select(Users).where(Users.id == id))
            user = result.scalar_one_or_none()
            if not user:
                raise HTTPException(status_code=422, detail="User not found")
            return UserVO(**row_to_dict(user))

    async def find_by_email(self, email: str) -> User:
        async with SessionLocal() as db:
            result = await db.execute(select(Users).where(Users.email == email))
            user = result.scalar_one_or_none()
            if not user:
                raise HTTPException(status_code=422, detail="User not found")
            return UserVO(**row_to_dict(user))

    async def save(self, user: User):
        new_user = Users(
            id=user.id,
            email=user.email,
            password_hash=user.password_hash,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        async with SessionLocal() as db:
            try:
                db.add(new_user)
                await db.commit()
            except SQLAlchemyError as e:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
                )
            except Exception as e:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
                )
            finally:
                await db.close()
