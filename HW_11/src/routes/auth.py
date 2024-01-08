from fastapi import Depends, HTTPException, status, APIRouter, BackgroundTasks, Request, Response
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.repository import users as repositories_users
from src.schemas.user import UserResponse, UserSchema, TokenSchema, RequestEmail
from src.services.auth import auth_service
from src.services.email import send_email
from src.conf import messages

router = APIRouter(prefix="/auth", tags=["auth"])
get_refresh_token = HTTPBearer()


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserSchema, bt: BackgroundTasks, request: Request, db: AsyncSession = Depends(get_db)):
    """
    The signup function creates a new user in the database.
        It takes in a UserSchema object, which is validated by pydantic.
        If the email already exists, it raises an HTTPException with status code 409 (Conflict).
        Otherwise, it hashes the password and creates a new user using create_user from repositories/users.py.

    :param body: UserSchema: Validate the request body
    :param bt: BackgroundTasks: Add a task to the background tasks queue
    :param request: Request: Get the base url of the request
    :param db: AsyncSession: Get the database session
    :return: A user object
    :doc-author: Trelent
    """
    exist_user = await repositories_users.get_user_by_username(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=messages.ACCOUNT_EXIST)
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repositories_users.create_user(body, db)
    bt.add_task(send_email, new_user.email, new_user.username, str(request.base_url))
    return new_user


@router.post("/login", response_model=TokenSchema)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """
    The login function is used to authenticate a user.
        It takes in the username and password of the user, verifies them against
        those stored in the database, and returns an access token if successful.

    :param body: OAuth2PasswordRequestForm: Validate the request body
    :param db: AsyncSession: Get the database session
    :return: A dictionary with the access token, refresh token and token type
    :doc-author: Trelent
    """
    user = await repositories_users.get_user_by_username(body.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not user.confirmed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed")
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repositories_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/refresh_token', response_model=TokenSchema)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(get_refresh_token),
                        db: AsyncSession = Depends(get_db)):
    """
    The refresh_token function is used to refresh the access token.
    It takes in a refresh token and returns a new access_token,
    refresh_token pair. The function first decodes the refresh token
    to get the email of the user who owns it. It then gets that user from
    the database and checks if their stored refresh_token matches what was passed in. If not, it raises an error because this means that either:

    :param credentials: HTTPAuthorizationCredentials: Get the access token from the header
    :param db: AsyncSession: Get the database session
    :return: A new access token and refresh token
    :doc-author: Trelent
    """
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repositories_users.get_user_by_username(email, db)
    if user.refresh_token != token:
        await repositories_users.update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repositories_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/confirmed_email/{token}')
async def confirmed_email(token: str, db: AsyncSession = Depends(get_db)):
    """
    The confirmed_email function is used to confirm a user's email address.
        It takes the token from the URL and uses it to get the user's email address.
        Then, it checks if that user exists in our database, and if they do not exist, returns an error message.
        If they do exist but their account has already been confirmed, we return a message saying so.
        Otherwise (if they are real and have not yet confirmed), we update their account status in our database.

    :param token: str: Get the token from the url
    :param db: AsyncSession: Get the database session
    :return: A message if the email is already confirmed or confirms it and returns a message
    :doc-author: Trelent
    """
    email = await auth_service.get_email_from_token(token)
    user = await repositories_users.get_user_by_username(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await repositories_users.confirmed_email(email, db)
    return {"message": "Email confirmed"}


@router.post('/request_email')
async def request_email(body: RequestEmail, background_tasks: BackgroundTasks, request: Request,
                        db: AsyncSession = Depends(get_db)):
    """
    The request_email function is used to send an email to the user with a link that will allow them
    to confirm their account. The function takes in a RequestEmail object, which contains the email of
    the user who wants to confirm their account. It then checks if there is already a confirmed account
    with that email address, and if so returns an error message saying as much. If not, it sends an
    email containing a confirmation link.

    :param body: RequestEmail: Get the email from the request body
    :param background_tasks: BackgroundTasks: Add a task to the background tasks queue
    :param request: Request: Get the base_url of the server
    :param db: AsyncSession: Get the database session
    :return: A message
    :doc-author: Trelent
    """
    user = await repositories_users.get_user_by_username(body.email, db)

    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        background_tasks.add_task(send_email, user.email, user.username, str(request.base_url))
    return {"message": "Check your email for confirmation."}


@router.get('/{username}')
async def request_username(username: str, response: Response, db: AsyncSession = Depends(get_db)):
    """
    The request_username function is a ReST endpoint that takes in a username and returns an image.
        The purpose of this function is to allow the user to open the link, which will then be logged by our server.
        This allows us to know when someone has opened their link.

    :param username: str: Get the username from the url
    :param response: Response: Set the status code of the response
    :param db: AsyncSession: Pass the database session to the function
    :return: A png image
    :doc-author: Trelent
    """
    print("______________________________________________________")
    print(f"{username} відкрив ссилку")
    print("______________________________________________________")
    return FileResponse("src/static/open_check.png", media_type="image/png", content_disposition_type="inline")
