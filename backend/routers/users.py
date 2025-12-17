from datetime import timedelta
from typing import List, Annotated

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from database import SessionDep
from models.user import User, UserCreate, UserRead, UserUpdate
from config.auth import (
    hash_password,
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from dependencies.dependency import CurrentUser
from config.logger_config import logger
router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserRead, status_code=201)
def create_user(
    user_create: UserCreate,
    session: SessionDep
):
    """
    Create a new user.

    :param user_create: UserCreate
    :param session: Database session
    :return: Created User
    """
    email_exists = session.exec(select(User).where(User.email == user_create.email)).first()
    if email_exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    username_exists = session.exec(select(User).where(User.username == user_create.username)).first()
    if username_exists:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_password = hash_password(user_create.password)
    
    db_user = User(
        username=user_create.username,
        email=user_create.email,
        password=hashed_password
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    logger.info(f"User created successfully: {db_user.username} (ID: {db_user.id})")
    return db_user

@router.get("/", response_model=List[UserRead])
def read_users(
    session: SessionDep,
    current_user: CurrentUser
):
    """
    Retrieve all users.

    :param session: Database session
    :param current_user: Currently authenticated user
    :return: List of Users
    """
    users = session.exec(select(User)).all()
    return users

@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    session: SessionDep,
    current_user: CurrentUser
):
    """
    Retrieve a user by ID.

    :param user_id: User ID
    :param session: Database session
    :param current_user: Currently authenticated user
    :return: User
    """
    user = session.get(User, user_id)
    if not user:
        logger.warning(f"User with ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: SessionDep,
    current_user: CurrentUser
):
    """
    Update a user's information.

    :param user_id: User ID
    :param user_update: UserUpdate
    :param session: Database session
    :param current_user: Currently authenticated user
    :return: Updated User
    """
    user = session.get(User, user_id)
    if not user:
        logger.warning(f"User with ID {user_id} not found for update")
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_update.username is not None:
        username_exists = session.exec(select(User).where(User.username == user_update.username, User.id != user_id)).first()
        if username_exists:
            logger.warning(f"Username {user_update.username} already taken")
            raise HTTPException(status_code=400, detail="Username already taken")
        user.username = user_update.username
    
    if user_update.email is not None:
        email_exists = session.exec(select(User).where(User.email == user_update.email, User.id != user_id)).first()
        if email_exists:
            raise HTTPException(status_code=400, detail="Email already registered")
        user.email = user_update.email

    if user_update.password is not None:
        user.password = hash_password(user_update.password)
    
    session.add(user)
    session.commit()
    session.refresh(user)
    logger.info(f"User with ID {user_id} updated successfully")
    return user

@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    session: SessionDep,
    current_user: CurrentUser
):
    """
    Delete a user by ID.

    :param user_id: User ID
    :param session: Database session
    :param current_user: Currently authenticated user
    :return: None
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    session.delete(user)
    session.commit()
    logger.info(f"User with ID {user_id} deleted successfully")
    return None

@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
):
    """
    Authenticate user and return access token.

    :param form_data: OAuth2PasswordRequestForm
    :param session: Database session
    :return: Access token
    """
    identifier = form_data.username
    password = form_data.password

    user = session.exec(
        select(User).where(
            (User.email == identifier) | (User.username == identifier)
        )
    ).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email/username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in_minutes": ACCESS_TOKEN_EXPIRE_MINUTES,
    }


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(current_user: CurrentUser):
    """
    Logout the current user.
    
    :param current_user: Currently authenticated user
    :return: RedirectResponse to home
    """
    response = RedirectResponse(url="/", status_code=302)
    # In a real application, you might want to implement token blacklisting here.
    # but for stateless JWT, logout is typically handled on the client side by deleting the token.
    # so in client applications, simply remove the token from storage.
    # so for this project, we keep it simple.
    return response