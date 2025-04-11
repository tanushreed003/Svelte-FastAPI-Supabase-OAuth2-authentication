# OAuth2 Authentication Backend

This backend uses FastAPI to handle Google and Kakao OAuth2 authentication.

## Installation

1. Install required packages:

```bash
pip install -r requirements.txt
```

2. Set environment variables:

Copy the `.env.example` file to create a `.env` file and configure the necessary environment variables:

- Supabase URL and service role key
- Google OAuth2 client ID and secret key
- Kakao OAuth2 client ID and secret key
- JWT secret key

## Running

Run the backend server:

```bash
python run.py
```

The server runs at http://localhost:3000 by default.

## API Endpoints

- `GET /api/auth/google` - Start Google OAuth2 login
- `GET /api/auth/callback/google` - Handle Google OAuth2 callback
- `GET /api/auth/kakao` - Start Kakao OAuth2 login
- `GET /api/auth/callback/kakao` - Handle Kakao OAuth2 callback
- `GET /api/auth/session` - Return currently logged in user information
- `POST /api/auth/logout` - Logout

## Database

This backend uses Supabase as its database and requires the following table:

### users table

```sql
CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  uuid UUID NOT NULL UNIQUE,
  display_name TEXT,
  email TEXT NOT NULL UNIQUE,
  phone TEXT,
  provider TEXT NOT NULL,
  provider_type TEXT NOT NULL DEFAULT 'social',
  user_status BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP WITHOUT TIME ZONE,
  last_sign_in_at TIMESTAMP WITHOUT TIME ZONE
);
``` 