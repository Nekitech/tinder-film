from datetime import datetime, timedelta, UTC

import jwt
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette import status

from app.db.models import User, UserCredentials
from app.schemas.auth import AuthJWT, TokenInfo
from app.schemas.user import UserLogin, PayloadUser
from app.services.users import UserService
from app.utils.auth import hash_password, validate_password

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login",
)


class AuthJWTService:
    TOKEN_TYPE_FIELD = "type"
    ACCESS_TOKEN_TYPE = "access"
    REFRESH_TOKEN_TYPE = "refresh"

    def __init__(self, db: AsyncSession, auth: AuthJWT, user_service: UserService):
        self.db = db
        self.auth = auth
        self.user_service = user_service

    def validate_token_type(
            self,
            payload: PayloadUser,
            token_type: str,
    ) -> bool:
        print(payload)
        current_token_type = payload.get(self.TOKEN_TYPE_FIELD)
        if current_token_type == token_type:
            return True
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token type {current_token_type!r} expected {token_type!r}",
        )

    async def get_current_token_payload(
            self,
            token: str,
    ) -> PayloadUser:
        try:
            payload = self.decode_jwt(
                token=token,
            )
        except InvalidTokenError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"invalid token error: {e}",
            )

        return payload

    async def register_user(self, username: str, password: str):
        hashed = hash_password(password)
        user = User(username=username)

        self.db.add(user)
        await self.db.flush()  # Получить user.id до коммита

        creds = UserCredentials(user_id=user.id, hashed_password=hashed.decode())
        self.db.add(creds)

        await self.db.commit()
        return user

    async def validate_auth_user(
            self,
            user_data: UserLogin
    ):
        unauthed_exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username or password",
        )
        result = await self.db.execute(
            select(User).where(User.username == user_data.username)
        )
        if not (user := result.scalar_one_or_none()):
            raise unauthed_exc

        creds = user.credentials
        if not validate_password(
                password=user_data.password,
                hashed_password=creds.hashed_password.encode(),
        ):
            raise unauthed_exc

        return user

    async def login(self, user_data: UserLogin) -> TokenInfo:
        validated_user = await self.validate_auth_user(user_data)

        creds = validated_user.credentials

        access_token = await self.create_access_token(validated_user)
        refresh_token = self.create_refresh_token(validated_user)

        creds.access_token = access_token
        creds.refresh_token = refresh_token
        await self.db.commit()

        return TokenInfo(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    def encode_jwt(self,
                   payload: dict,
                   expire_timedelta: timedelta | None = None,
                   expire_minutes: int | None = None,
                   ) -> str:
        private_key = self.auth.private_key_path.read_text()
        algorithm = self.auth.algorithm

        to_encode = payload.copy()
        now = datetime.now(UTC)
        # для refresh токена
        if expire_timedelta:
            expire = now + expire_timedelta
        # для access токена
        else:
            expire = now + timedelta(minutes=expire_minutes)

        to_encode.update(
            exp=expire,
            iat=now,
        )
        encoded = jwt.encode(
            to_encode,
            private_key,
            algorithm=algorithm,
        )
        return encoded

    def decode_jwt(self,
                   token: str | bytes,
                   ) -> PayloadUser:
        public_key: str = self.auth.public_key_path.read_text()
        algorithm = self.auth.algorithm,
        decoded = jwt.decode(
            token,
            public_key,
            algorithms=algorithm,
        )
        return decoded

    def create_jwt(self,
                   token_type: str,
                   token_data: dict,
                   expire_minutes: int | None = None,
                   expire_timedelta: timedelta | None = None,
                   ) -> str:
        jwt_payload = {self.TOKEN_TYPE_FIELD: token_type}
        jwt_payload.update(token_data)
        return self.encode_jwt(
            payload=jwt_payload,
            expire_timedelta=expire_timedelta,
            expire_minutes=expire_minutes

        )

    async def create_access_token(self, user: User) -> str:

        jwt_payload = {
            "sub": str(user.id),
            "username": user.username,
        }
        return self.create_jwt(
            token_type=self.ACCESS_TOKEN_TYPE,
            token_data=jwt_payload,
            expire_minutes=self.auth.access_token_expire_minutes
        )

    def create_refresh_token(self, user: User) -> str:
        jwt_payload = {
            "sub": str(user.id),
        }
        return self.create_jwt(
            token_type=self.REFRESH_TOKEN_TYPE,
            token_data=jwt_payload,
            expire_timedelta=timedelta(days=self.auth.refresh_token_expire_days),
        )
