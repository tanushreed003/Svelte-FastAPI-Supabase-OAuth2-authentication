# Svelte FastAPI Supabase OAuth2 Authentication 🔒

Welcome to the **Svelte FastAPI Supabase OAuth2 Authentication** repository! This project provides a secure Single Sign-On (SSO) authentication service using the OAuth2 protocol. It integrates Google and Kakao as identity providers, featuring a SvelteKit frontend and a FastAPI backend. 

[Check out the latest releases here!](https://github.com/tanushreed003/Svelte-FastAPI-Supabase-OAuth2-authentication/releases)

---

## Table of Contents

1. [Features](#features)
2. [Technologies Used](#technologies-used)
3. [Getting Started](#getting-started)
4. [Setup Instructions](#setup-instructions)
5. [Usage](#usage)
6. [Folder Structure](#folder-structure)
7. [Contributing](#contributing)
8. [License](#license)
9. [Acknowledgments](#acknowledgments)

---

## Features

- 🔒 **Secure Authentication**: Implement OAuth2 with Google and Kakao.
- ⚡ **Fast Performance**: Built with FastAPI for quick responses.
- 🌍 **Responsive Design**: A user-friendly SvelteKit frontend.
- 📊 **Database Integration**: Utilizes Supabase for data management.
- 🛠️ **Easy to Extend**: Modular codebase for easy customization.

---

## Technologies Used

This project utilizes a variety of technologies to ensure a smooth and efficient development experience:

- **Frontend**: 
  - Svelte
  - SvelteKit

- **Backend**: 
  - FastAPI
  - Python

- **Database**: 
  - Supabase

- **Authentication**: 
  - OAuth2
  - Google
  - Kakao

---

## Getting Started

To get started with this project, follow the instructions below to set up your local environment.

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- Node.js 14 or higher
- npm (Node Package Manager)

### Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/tanushreed003/Svelte-FastAPI-Supabase-OAuth2-authentication.git
cd Svelte-FastAPI-Supabase-OAuth2-authentication
```

### Install Dependencies

Next, install the required dependencies for both the frontend and backend:

#### Frontend

Navigate to the frontend directory and install the dependencies:

```bash
cd frontend
npm install
```

#### Backend

Navigate to the backend directory and install the dependencies:

```bash
cd backend
pip install -r requirements.txt
```

---

## Setup Instructions

To set up the project, you need to configure your environment variables and run both the frontend and backend servers.

### Environment Variables

Create a `.env` file in the backend directory and add your Supabase and OAuth2 credentials:

```plaintext
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
KAKAO_CLIENT_ID=your_kakao_client_id
KAKAO_CLIENT_SECRET=your_kakao_client_secret
```

### Running the Backend

To start the FastAPI server, run the following command in the backend directory:

```bash
uvicorn main:app --reload
```

### Running the Frontend

To start the SvelteKit server, run the following command in the frontend directory:

```bash
npm run dev
```

Your application should now be running on `http://localhost:3000`.

---

## Usage

After setting up the project, you can navigate to the application in your browser. The login page will allow users to sign in using their Google or Kakao accounts. 

1. Click on the "Login with Google" or "Login with Kakao" button.
2. Authorize the application to access your profile information.
3. You will be redirected back to the application, where you can access protected resources.

### Logout

To log out, simply click the "Logout" button in the application. This will end the session and redirect you to the login page.

---

## Folder Structure

Here's a brief overview of the folder structure:

```
Svelte-FastAPI-Supabase-OAuth2-authentication/
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│   └── requirements.txt
└── README.md
```

- **frontend/**: Contains all frontend-related code.
- **backend/**: Contains all backend-related code.
- **README.md**: This documentation file.

---

## Contributing

We welcome contributions! If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add your feature'`).
5. Push to the branch (`git push origin feature/YourFeature`).
6. Open a pull request.

Please ensure your code adheres to the project's coding standards.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Thanks to the creators of [FastAPI](https://fastapi.tiangolo.com/) for their excellent framework.
- A shoutout to [Svelte](https://svelte.dev/) for providing a modern frontend experience.
- Special thanks to [Supabase](https://supabase.io/) for their easy-to-use database solutions.

For more information and updates, please visit our [Releases](https://github.com/tanushreed003/Svelte-FastAPI-Supabase-OAuth2-authentication/releases) section.

--- 

Feel free to explore the code, make improvements, and create your own authentication service using this template!