from ninja import Router
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.tokens import RefreshToken

from authentication.schemes import UserLoginSchema, TokenSchema, RegistrationSchema, TokenUpdateSchema, ProfileSchema
from authentication.services import login_user, registration, update_token, logout, get_profile
from catalog.schemes import ErrorSchema

router = Router(tags=['authentication'])


@router.post('login/', response={200: TokenSchema, 400: ErrorSchema})
def login(request, data: UserLoginSchema):
    return login_user(data.dict())


@router.post('registration/', response={200: TokenSchema, 400: ErrorSchema})
def registration_(request, data: RegistrationSchema):
    return registration(data.dict())


@router.post('update_token/', response={200: TokenSchema, 400: ErrorSchema})
def update_token_(request, data: TokenUpdateSchema):
    return update_token(request, data.dict())


@router.post('logout/', response={200: TokenSchema, 400: ErrorSchema}, auth=JWTAuth())
def logout_(request, data: TokenUpdateSchema):
    return logout(request, data.dict())


@router.get('profile/', response={200: ProfileSchema, 400: ErrorSchema}, auth=JWTAuth())
def profile(request):
    return get_profile(request)
