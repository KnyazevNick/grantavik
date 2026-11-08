from datetime import datetime, timezone, timedelta
from secrets import compare_digest

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.users.schemas import UserLogin, UserRead
from app.users.passwords import hash_password, verify_password
from app.users.models import User, Role, UserRole

from app.db import SessionFactory
from app.config import settings



class UsernameAlreadyTakenError(Exception):
    pass

class PasswordChangeRequiredError(Exception):
    pass



def create_globalhead(user: UserLogin, secret: str) -> UserRead:
    if not settings.bootstrap_secret:
        raise ValueError("Bootstrap authorization failed")
    
    same = compare_digest(
        secret.encode("utf-8"),
        settings.bootstrap_secret.encode("utf-8"),
    )
    if not same:
        raise ValueError("Bootstrap authorization failed")
    
    with SessionFactory() as session:
        statement = (
            select(Role)
            .where(Role.name == "global_head")
            .with_for_update()
        )
        role = session.scalar(statement)

        if role is None:
            raise ValueError("failed to find role global_head")
        existing_globalhead_statement = (
            select(UserRole)
            .where(UserRole.role_id == role.id)
        )
        global_head = session.scalar(existing_globalhead_statement)

        if global_head is not None:
            raise ValueError("user with global head is already exist!")

        new_globalhead = User(
            username=user.username,
            password_hash=hash_password(user.password),
        )
        session.add(new_globalhead)

        try:
            session.flush()
            add_user_role(session, new_globalhead.id, role.id)
            session.commit()
        except IntegrityError as error:
            session.rollback()

            sqlstate = getattr(error.orig, "sqlstate", None)
            diagnostic = getattr(error.orig, "diag", None)
            constraint_name = getattr(diagnostic, "constraint_name", None)

            if sqlstate == "23505" and constraint_name == "users_username_key":
                raise ValueError("Username is already taken")

            raise

        return UserRead.model_validate(new_globalhead)


def get_user_by_id(user_id: int) -> UserRead | None:
    """search user by id, return UserRead if found or None"""
    with SessionFactory() as session:
        statement = select(User).where(User.id == user_id)
        user = session.scalar(statement)
        if user is None:
            return None

        return UserRead.model_validate(user)


def get_user_by_username(username: str) -> UserRead | None:
    """search user by username, return UserRead if found or None"""
    with SessionFactory() as session:
        statement = select(User).where(User.username == username)
        user = session.scalar(statement)
        if user is None:
            return None

        return UserRead.model_validate(user)


def get_user_role_names(user_id: int) -> list[str]:
    """Return user roles."""
    with SessionFactory() as session:
        statement = (
            select(Role.name)
            .join(UserRole, UserRole.role_id == Role.id)
            .where(UserRole.user_id == user_id)
        )
        return session.scalars(statement).all()


def add_user_role(session: Session, user_id: int, role_id: int) -> None:
    new_role = UserRole(
        user_id=user_id,
        role_id=role_id,
    )
    session.add(new_role)


def check_user(credentials: UserLogin) -> UserRead | None:
    with SessionFactory() as session:
        statement = select(User).where(User.username == credentials.username)
        user = session.scalar(statement)
        if user is None:
            return None
        verify = verify_password(credentials.password, user.password_hash)
        if verify is False:
            return None
        
        date = user.temporary_password_expires_at
        if date is not None:
            raise PasswordChangeRequiredError

        return UserRead.model_validate(user)


def can_create_user_with_role(creator_roles: list[str], requested_role: str) -> bool:
    #role and who can create user with this role
    rules = {
        "employee": ["it_admin", "global_head"],
        "manager": ["it_admin", "global_head"],
        "resource_owner": ["it_admin", "global_head"],
        "it_admin": ["global_head"],
        "global_head": [],
    }

    allowed_creator_roles = rules.get(requested_role, [])

    for role in creator_roles:
        if role in allowed_creator_roles:
            return True
    return False


def create_user_with_role(
    username: str,
    password: str,
    role_name: str,
    ) -> UserRead:
    password_hash = hash_password(password)

    with SessionFactory() as session:
        statement = select(Role).where(Role.name == role_name)
        role = session.scalar(statement)
        if role is None:
            raise ValueError("failed to find role")

        expires_at = datetime.now(timezone.utc) + timedelta(hours=24)
        new_user = User(
            username=username,
            password_hash=password_hash,
            temporary_password_expires_at=expires_at,
        )
        session.add(new_user)
        try:
            session.flush()
            add_user_role(session, new_user.id, role.id)
            user = UserRead.model_validate(new_user)
            session.commit()
        except IntegrityError as error:
            session.rollback()

            sqlstate = getattr(error.orig, "sqlstate", None)
            diagnostic = getattr(error.orig, "diag", None)
            constraint_name = getattr(diagnostic, "constraint_name", None)

            if sqlstate == "23505" and constraint_name == "users_username_key":
                raise UsernameAlreadyTakenError(
                    "Username is already taken",
                ) from error

            raise

        return user