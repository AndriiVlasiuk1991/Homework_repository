from fastapi import Request, Depends, HTTPException, status

from src.entity.models import User, Role
from src.services.auth import auth_service


class RoleAccess:
    def __init__(self, allowed_roles: list[Role]):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the instance of the class, and takes arguments that are passed to it.
        In this case, we're taking a list of allowed roles as an argument.

        :param self: Represent the instance of the class
        :param allowed_roles: list[Role]: Create a list of allowed roles
        :return: Nothing
        :doc-author: Trelent
        """
        self.allowed_roles = allowed_roles

    async def __call__(self, request: Request, user: User = Depends(auth_service.get_current_user)):
        """
        The __call__ function is the function that will be called when a user tries to access an endpoint.
        It takes in two arguments: request and user. The request argument is the Request object, which contains all of
        the information about the incoming HTTP request (headers, body, etc.). The second argument depends on whether or not
        you have defined a dependency for this route. In our case we are using Depends(auth_service.get_current_user) as our
        dependency so it will call auth_service's get current user function and pass in whatever it returns as the second argument.

        :param self: Access the class attributes
        :param request: Request: Get the request object
        :param user: User: Get the current user, and the request: request parameter is used to get information about the current request
        :return: A function that takes a request and user as arguments
        :doc-author: Trelent
        """
        print(user.role, self.allowed_roles)
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="FORBIDDEN",
            )

