import json
import os
import uuid
from datetime import datetime, timedelta
from typing import Optional

import httpx
from app.auth import create_access_token, get_current_user, verify_token
from app.database import get_supabase_client
from app.models import OAuthProvider, User, UserCreate, UserResponse
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

load_dotenv()

app = FastAPI(
    title="OAuth2 Authentication API",
    description="API for handling Google and Kakao OAuth2 authentication",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:4173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:3000/api/auth/callback/google")

KAKAO_CLIENT_ID = os.getenv("KAKAO_CLIENT_ID")
KAKAO_CLIENT_SECRET = os.getenv("KAKAO_CLIENT_SECRET")
KAKAO_REDIRECT_URI = os.getenv("KAKAO_REDIRECT_URI", "http://localhost:3000/api/auth/callback/kakao")

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRATION_MINUTES = int(os.getenv("JWT_EXPIRATION_MINUTES", "60"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/api/auth/google")
async def google_login():
    """Start Google OAuth2 login"""
    auth_url = f"https://accounts.google.com/o/oauth2/auth"
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "email profile",
        "access_type": "offline",
        "prompt": "consent",
    }

    query_string = "&".join([f"{key}={value}" for key, value in params.items()])
    authorization_url = f"{auth_url}?{query_string}"

    return RedirectResponse(url=authorization_url)


@app.get("/api/auth/callback/google")
async def google_callback(code: str):
    """Handle Google OAuth2 callback"""
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": GOOGLE_REDIRECT_URI,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)
        token_data = response.json()

        if "error" in token_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error getting Google access token: {token_data['error']}",
            )

        access_token = token_data["access_token"]
        user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}

        user_response = await client.get(user_info_url, headers=headers)
        user_info = user_response.json()

        supabase = get_supabase_client()

        response = supabase.table("users").select("*").eq("email", user_info["email"]).execute()
        user_data = response.data

        now = datetime.now().isoformat()

        if not user_data:
            new_user = {
                "uuid": str(uuid.uuid4()),
                "display_name": user_info.get("name", ""),
                "email": user_info["email"],
                "phone": "",
                "provider": "google",
                "provider_type": "social",
                "user_status": True,
                "created_at": now,
                "last_sign_in_at": now,
            }

            response = supabase.table("users").insert(new_user).execute()
            user_data = response.data
            user = user_data[0] if user_data else new_user
        else:
            user = user_data[0]
            update_data = {"last_sign_in_at": now}

            supabase.table("users").update(update_data).eq("uuid", user["uuid"]).execute()

        access_token = create_access_token(
            data={"sub": user["uuid"], "email": user["email"]}, expires_delta=timedelta(minutes=JWT_EXPIRATION_MINUTES)
        )

        redirect_url = f"{FRONTEND_URL}/auth/callback?token={access_token}"
        return RedirectResponse(url=redirect_url)


@app.get("/api/auth/kakao")
async def kakao_login():
    """Start Kakao OAuth2 login"""
    auth_url = "https://kauth.kakao.com/oauth/authorize"
    params = {
        "client_id": KAKAO_CLIENT_ID,
        "redirect_uri": KAKAO_REDIRECT_URI,
        "response_type": "code",
    }

    query_string = "&".join([f"{key}={value}" for key, value in params.items()])
    authorization_url = f"{auth_url}?{query_string}"

    return RedirectResponse(url=authorization_url)


@app.get("/api/auth/callback/kakao")
async def kakao_callback(code: str):
    """Handle Kakao OAuth2 callback"""
    token_url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": KAKAO_CLIENT_ID,
        "client_secret": KAKAO_CLIENT_SECRET,
        "code": code,
        "redirect_uri": KAKAO_REDIRECT_URI,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)
        token_data = response.json()

        if "error" in token_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error getting Kakao access token: {token_data['error']}",
            )

        access_token = token_data["access_token"]
        user_info_url = "https://kapi.kakao.com/v2/user/me"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }

        user_response = await client.get(user_info_url, headers=headers)
        user_info = user_response.json()

        kakao_account = user_info.get("kakao_account", {})
        profile = kakao_account.get("profile", {})
        email = kakao_account.get("email", f"kakao_{user_info['id']}@example.com")

        supabase = get_supabase_client()

        response = supabase.table("users").select("*").eq("email", email).execute()
        user_data = response.data

        now = datetime.now().isoformat()

        if not user_data:
            new_user = {
                "uuid": str(uuid.uuid4()),
                "display_name": profile.get("nickname", ""),
                "email": email,
                "phone": "",
                "provider": "kakao",
                "provider_type": "social",
                "user_status": True,
                "created_at": now,
                "last_sign_in_at": now,
            }

            response = supabase.table("users").insert(new_user).execute()
            user_data = response.data
            user = user_data[0] if user_data else new_user
        else:
            user = user_data[0]
            update_data = {"last_sign_in_at": now}

            supabase.table("users").update(update_data).eq("uuid", user["uuid"]).execute()

        access_token = create_access_token(
            data={"sub": user["uuid"], "email": user["email"]}, expires_delta=timedelta(minutes=JWT_EXPIRATION_MINUTES)
        )

        redirect_url = f"{FRONTEND_URL}/auth/callback?token={access_token}"
        return RedirectResponse(url=redirect_url)


@app.get("/api/auth/session", response_model=UserResponse)
async def get_session(current_user: User = Depends(get_current_user)):
    """Get current session information"""
    return current_user


@app.post("/api/auth/logout")
async def logout():
    """Logout from the current session"""
    return JSONResponse(content={"message": "Logged out successfully"})


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "OAuth2 Authentication API"}
