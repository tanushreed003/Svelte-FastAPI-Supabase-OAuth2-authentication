<img src="images/Svelte-FastAPI-Supabase-OAuth2-authentication.png"/>

This project is an application that implements OAuth2 SSO authentication for Google and Kakao using a SvelteKit frontend and FastAPI backend.

## Project Structure

- `src/` - SvelteKit frontend code
- `backend/` - FastAPI backend code

## Features

- Google OAuth2 login
- Kakao OAuth2 login
- JWT-based authentication
- User information storage using Supabase database

## Installation and Setup

### Frontend (SvelteKit)

1. Install required packages:

```bash
pnpm install
```

2. Run development server:

```bash
pnpm run dev
```

The frontend runs at http://localhost:5173 by default.

### Backend (FastAPI)

1. Navigate to the backend directory:

```bash
cd backend
```

2. Install required packages:

```bash
pip install -r requirements.txt
```

3. Set environment variables:

Copy the `.env.example` file to create a `.env` file and configure the necessary environment variables:

```bash
cp .env.example .env
```

4. Run the backend server:

```bash
python run.py
```

The backend runs at http://localhost:3000 by default.

## Database Setup

This project uses Supabase as its database. The following table is required:

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

## OAuth Provider Setup

### Google OAuth2

1. Create a project in the [Google Cloud Console](https://console.cloud.google.com/).
2. Generate an OAuth client ID in API & Services > Credentials.
3. Add `http://localhost:3000/api/auth/callback/google` as an authorized redirect URI.
4. Add the client ID and secret key to the backend `.env` file.

### Kakao OAuth2

1. Create an application on [Kakao Developers](https://developers.kakao.com/).
2. Add `http://localhost:5173` as a site domain in Platform > Web.
3. Configure Kakao Login in Product Settings.
4. Add `http://localhost:3000/api/auth/callback/kakao` as a redirect URI.
5. Add the REST API key and Client Secret to the backend `.env` file.

## Security Considerations

- Always use secure HTTPS connections in production environments.
- Keep your JWT secret key strong and secure.
- Store user information with appropriate access management.
