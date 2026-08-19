import uuid
from datetime import datetime, timezone

from boto3.dynamodb.conditions import Key
from fastapi import APIRouter, HTTPException, status

from app.models.user import UserSignup, UserLogin
from app.database.dynamodb import users_table
from app.core.security import hash_password, verify_password, create_access_token


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post("/signup")
def signup(request: UserSignup):
    login_id = request.login_id.strip().lower()
    email = request.email.lower()

    login_response = users_table.query(
        IndexName="login_id-index",
        KeyConditionExpression=Key("login_id").eq(login_id)
    )

    if login_response.get("Items"):
        raise HTTPException(
            status_code=400,
            detail="Login ID already exists"
        )

    email_response = users_table.query(
        IndexName="email-index",
        KeyConditionExpression=Key("email").eq(email)
    )

    if email_response.get("Items"):
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    user_id = str(uuid.uuid4())

    user = {
        "user_id": user_id,
        "login_id": login_id,
        "first_name": request.first_name.strip(),
        "last_name": request.last_name.strip(),
        "email": email,
        "password_hash": hash_password(request.password),
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    users_table.put_item(Item=user)

    token = create_access_token(user_id)

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "user_id": user_id,
            "login_id": user["login_id"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "email": user["email"]
        }
    }


@router.post("/login")
def login(request: UserLogin):
    response = users_table.query(
        IndexName="login_id-index",
        KeyConditionExpression=Key("login_id").eq(
            request.login_id.strip().lower()
        )
    )

    users = response.get("Items", [])

    if not users:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login ID or password"
        )

    user = users[0]

    if not verify_password(
        request.password,
        user["password_hash"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login ID or password"
        )

    token = create_access_token(user["user_id"])

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "user_id": user["user_id"],
            "login_id": user["login_id"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "email": user["email"]
        }
    }
