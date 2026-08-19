from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user


router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {
        "user_id": current_user["user_id"],
        "login_id": current_user["login_id"],
        "first_name": current_user["first_name"],
        "last_name": current_user["last_name"],
        "email": current_user["email"]
    }
