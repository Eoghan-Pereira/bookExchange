# Book Exchange

A web application for exchanging books. Users can sign up, log in, and reset their passwords. The application supports email/password authentication and Google login.

## Features

- User Signup
- User Login
- Password Reset
- Google Authentication

## Technologies Used

- Svelte
- python
- TypeScript
- Tailwind CSS

## Setup Instructions

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/bookExchange.git
   cd bookExchange
   npm install
   npm run dev
   ```
   in a new terminal
   ```sh
   cd backend
   python -m uvicorn main:app --reload

   ```
## Project Structure

- `src/routes/signup/+page.svelte`: Signup page
- `src/routes/login/+page.svelte`: Login page
- `src/routes/forgot-password/+page.svelte`: Password reset page
- `src/lib/auth.ts`: Authentication functions

## Page Details

### Signup Page (`src/routes/signup/+page.svelte`)

Allows users to create a new account using their email and password. Users can also sign up using their Google account.

- **Fields**: Email, Password, Confirm Password
- **Actions**: Sign Up, Sign Up with Google
- **Navigation**: Link to Login page

### Login Page (`src/routes/login/+page.svelte`)

Allows users to log in to their account using their email and password. Users can also log in using their Google account.

- **Fields**: Email, Password
- **Actions**: Login, Login with Google
- **Navigation**: Links to Signup and Forgot Password pages

### Forgot Password Page (`src/routes/forgot-password/+page.svelte`)

Allows users to reset their password by entering their email address. A password reset link will be sent to the provided email.

- **Fields**: Email
- **Actions**: Send Reset Link
- **Navigation**: Link to Login page

## Authentication Functions

- `signUpWithEmail(email: string, password: string)`: Sign up with email and password
- `loginWithEmail(email: string, password: string)`: Log in with email and password
- `loginWithGoogle()`: Log in with Google
- `resetPassword(email: string)`: Reset password

