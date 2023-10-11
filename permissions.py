# import jwt
# from fastapi.security import OAuth2PasswordBearer
# from fastapi import Depends, HTTPException, Security
# from starlette.status import HTTP_403_FORBIDDEN
#
# from myapp.user import models, crud, schemas
#
#
# SECRET_KEY = "udfsdu6%$&(*Y9dHG(&ytdf987gFST*Sg897"
# ALGORITHM = "HS256"
# reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/login/access-token")
#
#
# def get_current_user(token: str = Security(reusable_oauth2)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         token_data = schemas.TokenPayload(**payload)
#     except jwt.PyJWTError:
#         raise HTTPException(
#             status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
#         )
#
#     if user := crud.user.get(id=token_data.user_id):
#         raise HTTPException(status_code=404, detail="User not found")
#     return user
#
#
# class PermissionsRouter:
#     def __init__(self, permissions: tuple):
#         self.permissions = permissions
#
#     def check_access(self, current_user: models.User):
#         for permission in current_user.permissions:
#             if permission.code_name in self.permissions:
#                 return current_user
#
#         raise HTTPException(status_code=400, detail="The user doesn't have enough privileges")
#
#     def __call__(self, user: models.User = Depends(get_current_user)):
#         return self.check_access(current_user=user)
