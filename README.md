# Lms-backend-
# DRF Project Documentation (Library Management System)

Welcome to the documentation for our Django REST Framework (DRF) project.

## Base URL

The base URL for this API is `https://lmsbackend-iibf.onrender.com`.

## Overview

Our project is designed to manage a library system, allowing librarians and members to register, manage user profiles, handle book inventory, borrow and return books, and more.

## Technologies Used

- Django
- Django REST Framework
- Django Simple JWT (JSON Web Tokens)

## API Endpoints

### User Registration

#### Librarian Registration

- **Endpoint:** `/register-librarian/`
- **Method:** `POST`
- **Description:** Register a new librarian.
- **Permissions:** Public

#### Member Registration

- **Endpoint:** `/register-member/`
- **Method:** `POST`
- **Description:** Register a new member.
- **Permissions:** Public

### User Management

#### Member Registration by Librarian

- **Endpoint:** `/meber-registration-by-librarian/`
- **Methods:** `GET`, `POST`
- **Description:** Librarians can view and register members.
- **Permissions:** Librarians only (IsAuthenticated)

#### Member Update and Delete

- **Endpoint:** `/meber-update-delete/<int:pk>/`
- **Methods:** `GET`, `PUT`, `DELETE`
- **Description:** Librarians can view, update, and delete member profiles.
- **Permissions:** Librarians only (IsAuthenticated)

#### User Profile

- **Endpoint:** `/profile/`
- **Method:** `GET`
- **Description:** View user profile information.
- **Permissions:** Authenticated users only (IsAuthenticated)

#### Delete User Profile

- **Endpoint:** `/profile/delete/`
- **Method:** `DELETE`
- **Description:** Delete the user profile.
- **Permissions:** Authenticated users only (IsAuthenticated)

### Authentication

#### User Login

- **Endpoint:** `/login/`
- **Method:** `POST`
- **Description:** Obtain a JWT token for authentication.
- **Permissions:** Public

#### User Logout

- **Endpoint:** `/logout/`
- **Method:** `POST`
- **Description:** Log out the user and invalidate the token.
- **Permissions:** Authenticated users only (IsAuthenticated)

### Book Management

#### List and Create Books

- **Endpoint:** `/books/`
- **Methods:** `GET`, `POST`
- **Description:** List all books and create a new book.
- **Permissions:** Authenticated users only (IsAuthenticated)

#### Retrieve, Update, and Delete Book

- **Endpoint:** `/books/<int:pk>/`
- **Methods:** `GET`, `PUT`, `DELETE`
- **Description:** Retrieve, update, or delete a specific book.
- **Permissions:** Authenticated users only (IsAuthenticated)

#### List Books for Members

- **Endpoint:** `/books-member/`
- **Method:** `GET`
- **Description:** List available books for members.
- **Permissions:** Authenticated users only (IsAuthenticated)

### Borrowing and Returning Books

#### Borrow Book

- **Endpoint:** `/books/<int:book_id>/borrow/`
- **Method:** `POST`
- **Description:** Borrow a book by a member.
- **Permissions:** Authenticated users only (IsAuthenticated)

#### Return Book

- **Endpoint:** `/transactions/<int:transaction_id>/return/`
- **Method:** `PATCH`
- **Description:** Return a borrowed book.
- **Permissions:** Authenticated users only (IsAuthenticated)

### Current User Information

#### Current User Profile

- **Endpoint:** `/current_user/`
- **Method:** `GET`
- **Description:** Retrieve information about the currently authenticated user.
- **Permissions:** Authenticated users only (IsAuthenticated)

